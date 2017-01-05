# -*- coding: utf-8 -*-

import socket
import threading
from Crypto.PublicKey import RSA
import base64
import Utils
import Database


class ClientThread(threading.Thread):
    def __init__(self, address, client):
        threading.Thread.__init__(self)
        self.address = address
        self.client = client
        self.daemon = True
        self.db = Database.Database()

    def whatdo(self, content):
        answer_to_client = None

        if content[0] == 'REG':
            answer_to_client = self.registration(content)

        answer_to_client.ljust(2048, '=')
        print len(answer_to_client)

        self.client.send(answer_to_client)


    def registration(self, data):
        msg = None
        pubkey_client = RSA.importKey(data[5])
        privkey_serv = RSA.importKey(open('priv_key.pem', 'r'))

        if self.db.check_nickname(data[1]) == False:
            self.db.add_user(data[1], data[2], data[3], data[5])
            msg = 'OK'
        else:
            msg = 'WRONG'

        msg = Utils.pgp_enc_msg(pubkey_client, privkey_serv, msg)

        return msg

    def run(self):
        msg = self.client.recv(8192)
        content = Utils.pgp_dec_msg('key', msg) ## choosing key need
        self.whatdo(content)


class Server(object):
    def __init__(self):
        self.PORT = 5000
        self.ADDRESS = 'localhost'

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.ADDRESS, self.PORT))
        self.server.listen(5)
        self.server_loop()

    def server_loop(self):
        while True:
            CLIENT, ADDRESS = self.server.accept()
            ct = ClientThread(ADDRESS, CLIENT)
            ct.run()

cos = Server