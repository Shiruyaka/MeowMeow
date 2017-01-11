# -*- coding: utf-8 -*-
#!/usr/bin/env python

import socket
import threading
from Crypto.PublicKey import RSA
import base64
import Utils
import Database
from Keyring import PrivateRing, PublicRing, find_pubkey_in_ring


class ClientThread(threading.Thread):
    def __init__(self, publicKeyRing, privateKeyRing, client):
        threading.Thread.__init__(self)

        self.publicKeyRing = publicKeyRing
        self.privateKeyRing = privateKeyRing
        self.client = client
        self.daemon = True
        self.db = Database.Database()
        #print self.privateKeyRing

    def whatdo(self, content):
        answer_to_client = None
        #print content
        if content[0] == 'REG':
            answer_to_client = self.registration(content)
        elif content[0] == 'LOG':
            answer_to_client = self.authentication(content)
        elif content[0] == 'CRM':
            answer_to_client = self.createroom(content)

        answer_to_client = answer_to_client.ljust(8192, '=')
        #print len(answer_to_client)

        self.client.send(answer_to_client)

    def createroom(self, content):

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

        return msg

    def authentication(self, data):
        key_client = RSA.importKey(find_pubkey_in_ring(self.publicKeyRing, whose=data[1]))
        key_server = RSA.importKey(self.privateKeyRing[0].priv_key)

        key_server_id = Utils.get_key_id(key_server.publickey())

        respond = self.db.verify(data[1], data[2])
        msg = None

        if len(respond) > 0:
            msg = 'RE|OK|' + Utils.make_msg(respond)
            print 'Valid'
        else:
            msg = 'RE|WRONG'
            print 'Wrong username or password'

        msg = msg + '|' + key_server_id

        return Utils.pgp_enc_msg(key_client, key_server, msg)

    def run(self):
        msg = self.client.recv(8192)
        content = Utils.pgp_dec_msg(msg, self.publicKeyRing, self.privateKeyRing) ## choosing key need
        self.whatdo(content)


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
        self.server.bind((self.ADDRESS, self.PORT))
        self.server.listen(5)

        print self.publicKeyRing
        self.server_loop()

    def server_loop(self):

        while True:
            CLIENT, ADDRESS = self.server.accept()
            ct = ClientThread(self.publicKeyRing, self.privateKeyRing, CLIENT)
            ct.run()

cos = Server
