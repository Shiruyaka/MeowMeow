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

    def decrypt(self, msg):
        Utils.pgp_dec_msg('key', msg)
#        priv_key =  RSA.importKey(open('priv_key.pem', 'r'))
 #       rsadecrypt = PKCS1_OAEP.new(priv_key)
  #      content = msg.split(';')
   #     sessionkey = rsadecrypt.decrypt(base64.b64decode(content[1]))
    #    aes = AES.new(sessionkey, AES.MODE_CBC, Utils.IV)
     #   msg_de = aes.decrypt(base64.b64decode(content[2])).split(';')
      #  msg_de[-1] = msg_de[-1].rstrip('=')
       # print msg_de
        #rsadecrypt.decrypt()
    def run(self):
        msg = self.client.recv(8192)
        self.decrypt(msg)



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