# -*- coding: utf-8 -*-
#!/usr/bin/env python

import socket
import threading
from Crypto.PublicKey import RSA
import Utils
import Database
import select
import Queue
from Keyring import PrivateRing, PublicRing, find_pubkey_in_ring, choose_randomly_enc_key


MESSAGES_TO_ROOM = Queue.Queue()

class Client(threading.Thread):
    def __init__(self, publicKeyRing, privateKeyRing, connection):
        threading.Thread.__init__(self)

        self.nick = None
        self.id = None

        self.publicKeyRing = publicKeyRing
        self.privateKeyRing = privateKeyRing

        self.connection = connection

        self.daemon = True


class ClientRecv(Client):
    def __init__(self, publicKeyRing, privateKeyRing, connection, client_send, rooms):
        Client.__init__(self, publicKeyRing, privateKeyRing, connection)

        self.client_send = client_send
        self.db = Database.Database()

        self.end_conn = False
        self.rooms = rooms


    def whatdo(self, content):
        answer_to_client = None

        if content[0] == 'REG':
            answer_to_client = self.registration(content)
        elif content[0] == 'LOG':
            answer_to_client = self.authentication(content)
        elif content[0] == 'CRM':
            answer_to_client = self.createroom(content)
        elif content[0] == 'LRM':
            answer_to_client = self.getlistofrooms(content)
        elif content[0] == 'KEY':
            answer_to_client = self.add_new_key(content)
        else:
            self.end_conn == True
            answer_to_client = 'NOT THIS TIME MALLORY'

        #print len(answer_to_client)
        answer_to_client = answer_to_client.ljust(8192, '=')
        self.client_send.data.put(answer_to_client)

        if self.end_conn == True:
            self.client_send.end_conn = True


    def add_new_key(self, data):

        client_key = find_pubkey_in_ring(self.publicKeyRing, whose=data[4])

        pub_key_id = Utils.get_key_id(RSA.importKey(data[2]))
        self.db.add_key(pub_key_id, data[3], data[2], data[1])
        self.publicKeyRing.append(PublicRing(data[1], pub_key_id, data[2], 0, data[4], 0))

        privkey, id = choose_randomly_enc_key(self.privateKeyRing)
        msg =  Utils.make_msg(['KEY', 'Done', id])

        msg = Utils.pgp_enc_msg(client_key, privkey, msg)
        return msg

    def getlistofrooms(self, data):

        lst_of_rooms = list()
        lst_of_rooms.append('LRM')

        for rm in self.rooms:
            if rm.signed < rm.lim_in_room and not rm.is_user_on_whitelist(self.nick):
                lst_of_rooms.append(rm.tostring())

        key_client = find_pubkey_in_ring(self.publicKeyRing, whose=self.nick)
        key_server = RSA.importKey(self.privateKeyRing[0].priv_key)
        key_server_id = Utils.get_key_id(key_server.publickey())

        lst_of_rooms.append(key_server_id)
        msg = Utils.make_msg(lst_of_rooms)


        return Utils.pgp_enc_msg(key_client, key_server, msg)

    def createroom(self, data):
        respond = self.db.create_room(data[2], data[4], data[1], data[3])
        key_client = find_pubkey_in_ring(self.publicKeyRing, whose=self.nick)
        key_server = RSA.importKey(self.privateKeyRing[0].priv_key)

        key_server_id = Utils.get_key_id(key_server.publickey())

        if respond != 0:
            msg = Utils.make_msg(('CRM', 'OK', respond, key_server_id))
        else:
            msg = Utils.make_msg(('CRM', 'WRONG', key_server_id))

        return Utils.pgp_enc_msg(key_client, key_server, msg)

    def registration(self, data):
        msg = None
        pubkey_client = RSA.importKey(data[7])
        privkey_serv = RSA.importKey(self.privateKeyRing[0].priv_key)
        key_id = self.privateKeyRing[0].key_id

        if self.db.check_nickname(data[1]) == False:
            id = self.db.add_user(data[1], data[2], data[3], data[4], data[5])
            pub_key_id = Utils.get_key_id(pubkey_client)
            self.db.add_key(pub_key_id, id, data[7], data[6])
            self.publicKeyRing.append(PublicRing(data[6], pub_key_id, data[7], 0, data[1], 0))
            msg = 'REGRES|OK'
        else:
            msg = 'REGRES|WRONG'

        msg = msg + '|' + key_id
        msg = Utils.pgp_enc_msg(pubkey_client, privkey_serv, msg)

        self.end_conn = True
        return msg

    def authentication(self, data):

        key_client = find_pubkey_in_ring(self.publicKeyRing, whose=data[1])

        if key_client is None:
            key_client = find_pubkey_in_ring(self.publicKeyRing, id=data[3])
        #else:
        #    key_client = RSA.importKey(key_client)

        key_server = RSA.importKey(self.privateKeyRing[0].priv_key)
        key_server_id = Utils.get_key_id(key_server.publickey())
        respond = self.db.verify(data[1], data[2])
        msg = None

        if len(respond) > 0:
            self.id = respond[0]
            self.nick = data[1]

            for i in self.rooms:
                if i.is_user_on_whitelist(self.nick):
                    respond.append(i.tostring())

            msg = 'LOG|OK|' + Utils.make_msg(respond)
            print 'Valid'
        else:
            msg = 'LOG|WRONG'
            print 'Wrong username or password'
            self.end_conn = True

        msg = msg + '|' + key_server_id
        return Utils.pgp_enc_msg(key_client, key_server, msg)

    def run(self):

        while not self.end_conn:

            try:
                readable, writable, exceptional = select.select([self.connection], [], [])

                if readable[0]:

                    msg = self.connection.recv(8192)

                    if msg is not '':
                        content = Utils.pgp_dec_msg(msg, self.publicKeyRing, self.privateKeyRing) ## choosing key need
                        self.whatdo(content)
                    else:
                        self.end_conn = True
                        self.client_send.end_conn = True

                    #code for send massage from room to client
            except IndexError:
                self.connection.close()
                print 'Client disconnect suddenly'
                break

class ClientSend(Client):


    def __init__(self, publicKeyRing, privateKeyRing, connection):
        Client.__init__(self, publicKeyRing, privateKeyRing, connection)
        self.end_conn = False
        self.data = Queue.Queue()

    def run(self):
         while not self.end_conn or not self.data.empty():
             try:
                 readable, writable, exceptional = select.select([], [self.connection], [self.connection])

                 if writable[0] and not self.data.empty():
                    msg = self.data.get()
                    self.connection.send(msg)
             except:
                 self.connection.close()
                 print 'Client disconnect suddenly'
                 self.end_conn = True




class Server(object):
    def __init__(self):
        self.PORT = 5000
        self.ADDRESS = 'localhost'

        self.privateKeyRing = list()
        self.db = Database.Database()

        self.publicKeyRing = self.db.get_keys_of_users()

        key = RSA.importKey(open('priv_key.pem', 'r'))
        id = Utils.get_key_id(key.publickey())
        self.privateKeyRing.append(PrivateRing('', id, key.publickey().exportKey(), key.exportKey()))

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((self.ADDRESS, self.PORT))
        self.server.listen(5)

        self.rooms = self.db.get_all_rooms()

        for i in self.rooms:
            i.add_usr_whitelist(self.db.get_room_participants(i.id))

        self.server_loop()

    # def giving_out_data(self):
    #
    #     while True:
    #         if not ClientThread.message_queue.empty():
    #             for t in threading.enumerate():
    #                 if t is ClientThread:
    #                     print 'jupi' ###na razie tylko, jeszcze trzeba roomy wczytac tutaj usi byc wysylanie do roomow

    def server_loop(self):
        connected_users = list()

        while True:
            CLIENT, ADDRESS = self.server.accept()
            c_send = ClientSend(self.publicKeyRing, self.privateKeyRing, CLIENT)
            c_recv = ClientRecv(self.publicKeyRing, self.privateKeyRing, CLIENT, c_send, self.rooms)

            connected_users.append((c_recv, c_send))
            c_send.start()
            c_recv.start()


