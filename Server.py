# -*- coding: utf-8 -*-
#!/usr/bin/env python

import socket
import threading
from Crypto.PublicKey import RSA
import base64
import Utils
import Database
from Client import PrivateRing, PublicRing


class ClientThread(threading.Thread):
    def __init__(self, publicKeyRing, privateKeyRing, client):
        threading.Thread.__init__(self)

        self.publicKeyRing = publicKeyRing
        self.privateKeyRing = privateKeyRing
        self.client = client
        self.daemon = True
        self.db = Database.Database()
        print self.privateKeyRing

    def whatdo(self, content):
        answer_to_client = None
        print content
        if content[0] == 'REG':
            answer_to_client = self.registration(content)

        answer_to_client = answer_to_client.ljust(8192, '=')
        print len(answer_to_client)

        self.client.send(answer_to_client)


    def registration(self, data):
        msg = None
        pubkey_client = RSA.importKey(data[7])
        #privkey_serv = RSA.importKey(open('priv_key.pem', 'r'))
        privkey_serv = RSA.importKey(self.privateKeyRing[0].priv_key)
        key_id = self.privateKeyRing[0].key_id
        #print self.privateKeyRing[0].priv_key

        if self.db.check_nickname(data[1]) == False:
            id = self.db.add_user(data[1], data[2], data[3], data[4], data[5])
            self.db.add_key(Utils.get_key_id(pubkey_client), id, data[7], data[6])
            ##### fill public key ring later
            msg = 'RE|OK'
        else:
            msg = 'RE|WRONG'

        msg = msg + '|' + key_id
        msg = Utils.pgp_enc_msg(pubkey_client, privkey_serv, msg)

        return msg

    def run(self):
        msg = self.client.recv(8192)
        content = Utils.pgp_dec_msg(msg, self.publicKeyRing, self.privateKeyRing) ## choosing key need
        self.whatdo(content)


class Server(object):
    def __init__(self):
        self.PORT = 5000
        self.ADDRESS = 'localhost'

        self.privateKeyRing = list()
        self.publicKeyRing = list()

        ############ uzupelnic trzeba publicKeyRing
        ############PrivateRing = namedtuple('PrivateRing', 'timestamp key_id pub_key priv_key')
        key = RSA.importKey(open('priv_key.pem', 'r'))
        id = Utils.get_key_id(key.publickey())

        self.privateKeyRing.append(PrivateRing('',id , key.publickey().exportKey(), key.exportKey()))
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.ADDRESS, self.PORT))
        self.server.listen(5)
        self.server_loop()

    def server_loop(self):
        while True:
            CLIENT, ADDRESS = self.server.accept()
            ct = ClientThread(self.publicKeyRing, self.privateKeyRing, CLIENT)
            ct.run()

cos = Server
