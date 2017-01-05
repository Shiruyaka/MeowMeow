# -*- coding: utf-8 -*-

import socket
import threading
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Cipher import AES
import base64
import Utils

class ClientThread(threading.Thread):
    def __init__(self, address, client):
        threading.Thread.__init__(self)
        self.address = address
        self.client = client
        self.daemon = True

    def run(self):
        msg = self.client.recv(8192)
        content = Utils.pgp_dec_msg('key', msg) ## choosing key need
        print content


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

cos = Server()