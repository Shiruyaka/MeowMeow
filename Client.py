# -*- coding: utf-8 -*-

import socket




class Client():
    def __init__(self, user_data, priv_keyring, pub_keyring):#id, login, password, firstName, secondName, mail):

        self.priv_keyring = priv_keyring
        self.pub_keyring = pub_keyring

        self. id = user_data[0]
        self.login = user_data[1]
        self.password = user_data[2]
        self.firstName = user_data[3]
        self.secondName = user_data[4]
        self.mail = user_data[5]

    def find_key_in_ring(self, typeOfKeyRing, id_key, type_of_searched_key):
        if typeOfKeyRing == 'pub':
            ring = self.pub_keyring
        else:
            ring = self.priv_keyring

        for key in ring:
            print(key)
            if key.key_id == id_key:
                if type_of_searched_key == 'pub':
                    return key.pub_key
                else:
                    return key.priv_key
