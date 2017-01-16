# -*- coding: utf-8 -*-
import threading
import socket
import select
import Queue
import Utils

class User():
    def __init__(self, user_data, priv_keyring, pub_keyring):#id, login, password, firstName, secondName, mail):

        self.priv_keyring = priv_keyring
        self.pub_keyring = pub_keyring

        self.id = user_data[0]
        self.login = user_data[1]
        self.password = user_data[2]
        self.firstName = user_data[3]
        self.secondName = user_data[4]
        self.mail = user_data[5]


class UserRecv(threading.Thread):

    def __init__(self, user_data, connection):
        threading.Thread.__init__(self)

        self.user = user_data
        self.connection = connection
        self.daemon = True
        self.end_conn = False

    def run(self):

        while not self.end_conn:
            readable, writable, exceptional = select.select([self.connection], [], [])

            if readable[0]:

                msg = self.connection.recv(8192)
                content = Utils.pgp_dec_msg(msg, self.user.pub_keyring, self.user.priv_keyring) ## choosing key need


class UserSend(threading.Thread):

    def __init__(self, user_data, connection):
        threading.Thread.__init__(self)

        self.user = user_data
        self.connection = connection
        self.daemon = True
        self.end_conn = False
        self.data = Queue.Queue()
    def run(self):

        while not self.end_conn:

            readable, writable, exceptional = select.select([], [self.connection], [])

            if writable[0] and self.data.empty():
                msg = self.data.get()
                self.connection.send(msg)

                    #to nie powinno byc w Keyring???
    # def find_key_in_ring(self, typeOfKeyRing, id_key, type_of_searched_key):
    #     if typeOfKeyRing == 'pub':
    #         ring = self.pub_keyring
    #     else:
    #         ring = self.priv_keyring
    #
    #     for key in ring:
    #         print(key)
    #         if key.key_id == id_key:
    #             if type_of_searched_key == 'pub':
    #                 return key.pub_key
    #             else:
    #                 return key.priv_key
