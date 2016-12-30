# -*- coding: utf-8 -*-

import socket
import threading


class ClientThread(threading.thread):
    def __init__(self, address, client):
        threading.Thread.__init__(self)
        self.address = address
        self.client = client

    def run(self):
        print "Odezwał się klient spod adresu: %s:%d" % (self.address[0], self.address[1])

        request = self.client.recv(1024)

        print "Odebrano zapytanie: %s" % request

        self.client.send("OK")
        self.client.close()


class Server(object):
    def __init__(self):
        self.PORT = 5000
        self.ADDRESS = 'localhost'

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.ADDRESS, self.PORT))
        self.server.listen(5)


    def server_loop(self):
        while True:
            CLIENT, ADDRESS = self.server.accept()

            print threading.activeCount()
            CLIENT_THREAD = threading.Thread(target=receive_data, args=(CLIENT, ADDRESS))
            CLIENT_THREAD.daemon = True
            CLIENT_THREAD.start()