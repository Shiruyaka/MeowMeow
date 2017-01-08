# -*- coding: utf-8 -*-

from Crypto.PublicKey import RSA
from Crypto import Random
import Database
import hashlib
import Utils
from time import gmtime, strftime




class Client():
    def __init__(self, login, password, firstName, secondName, mail):
        self.db = Database.Database()
        self.priv_keyring = list()
        self.pub_keyring = list()
        self.login = login
        self.password = password
        self.firstName = firstName
        self.secondName = secondName
        self.mail = mail


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
