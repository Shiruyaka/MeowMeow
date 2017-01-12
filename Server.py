# -*- coding: utf-8 -*-
#!/usr/bin/env python

import socket
import threading
from Crypto.PublicKey import RSA
import base64
import Utils
import Database
import select
import Queue
from Keyring import PrivateRing, PublicRing, find_pubkey_in_ring

class ClientThread(threading.Thread):
    message_queue = Queue.Queue()

    def __init__(self, publicKeyRing, privateKeyRing, client):
        threading.Thread.__init__(self)

        self.client = client

        self.nick = None
        self.id = None

        self.publicKeyRing = publicKeyRing
        self.privateKeyRing = privateKeyRing
        self.db = Database.Database()

        self.daemon = True
        self.end_conn = False

        self.data = None
        self.isSending = False

    def whatdo(self, content):
        answer_to_client = None

        if content[0] == 'REG':
            answer_to_client = self.registration(content)
        elif content[0] == 'LOG':
            answer_to_client = self.authentication(content)
        elif content[0] == 'CRM':
            answer_to_client = self.createroom(content)

        answer_to_client = answer_to_client.ljust(8192, '=')


        self.client.send(answer_to_client)

    def createroom(self, data):
        respond = self.db.create_room(data[2], data[5], data[1], data[3], data[4])
        key_client = RSA.importKey(find_pubkey_in_ring(self.publicKeyRing, whose=self.nick))



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
            msg = 'RE|OK'
        else:
            msg = 'RE|WRONG'

        msg = msg + '|' + key_id
        msg = Utils.pgp_enc_msg(pubkey_client, privkey_serv, msg)

        self.end_conn = True
        return msg

    def authentication(self, data):
        key_client = RSA.importKey(find_pubkey_in_ring(self.publicKeyRing, whose=data[1]))
        key_server = RSA.importKey(self.privateKeyRing[0].priv_key)

        key_server_id = Utils.get_key_id(key_server.publickey())

        respond = self.db.verify(data[1], data[2])
        msg = None

        if len(respond) > 0:
            self.id = respond[0]
            self.nick = data[1]

            msg = 'RE|OK|' + Utils.make_msg(respond)
            print 'Valid'
        else:
            msg = 'RE|WRONG'
            print 'Wrong username or password'
            self.end_conn = True

        msg = msg + '|' + key_server_id

        return Utils.pgp_enc_msg(key_client, key_server, msg)

    def run(self):
        ready = select.select([self.client],[],[])

        while not self.end_conn:

            if ready[0]:
                self.isSending = True
                msg = self.client.recv(8192)
                content = Utils.pgp_dec_msg(msg, self.publicKeyRing, self.privateKeyRing) ## choosing key need
                self.whatdo(content)
                self.isSending = False
            elif self.data:
                self.isSending = True

                self.isSending = False
                #code for send massage from room to client



class Server(object):
    def __init__(self):
        self.PORT = 5000
        self.ADDRESS = 'localhost'

        self.privateKeyRing = list()
        self.db = Database.Database()

        self.publicKeyRing = self.db.get_keys_of_users()

        key = RSA.importKey(open('priv_key.pem', 'r'))
        id = Utils.get_key_id(key.publickey())
        self.privateKeyRing.append(PrivateRing('',id , key.publickey().exportKey(), key.exportKey()))

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((self.ADDRESS, self.PORT))
        self.server.listen(5)

        self.rooms = list()
        self.server_loop()

    def giving_out_data(self):

        while True:
            if not ClientThread.message_queue.empty():
                for t in threading.enumerate():
                    if t is ClientThread:
                        print 'jupi' ###na razie tylko, jeszcze trzeba roomy wczytac tutaj usi byc wysylanie do roomow

    def server_loop(self):
        i = 0
        while True:
            CLIENT, ADDRESS = self.server.accept()
            i = i + 1
            print i
            ct = ClientThread(self.publicKeyRing, self.privateKeyRing, CLIENT)
            ct.run()