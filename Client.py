# -*- coding: utf-8 -*-

from Crypto.PublicKey import RSA
from Crypto import Random
from collections import namedtuple
import Database
import hashlib
import Utils

PrivateRing = namedtuple('PrivateRing', 'timestamp key_id pub_key priv_key')
PublicRing  = namedtuple('PublicRing', 'timestamp key_id pub_key owner_trust user_id key_legit')


class Client():
    def __init__(self):
        self.db = Database.Database()
        self.priv_keyring = list()
        self.pub_keyring = list()

    def export_keyring(self, typeOfKeyRing):
        if typeOfKeyRing == 'pub':
            ring = self.pub_keyring
        else:
            ring = self.priv_keyring

        with open(typeOfKeyRing + '_keyring.txt', 'w') as w:
            for key in ring:
                record = ''
                for attr in key:
                    record += attr + '|'
                record = record.rstrip('|')
                w.write(record)

    def import_keyring(self, typeOfKeyRing):
        with open(typeOfKeyRing + '_keyring.txt', 'r') as r:
            data = r.readlines()
            for line in data:
                line = line.rstrip().split('|')
                if typeOfKeyRing == 'priv':
                    self.priv_keyring.append(PrivateRing(*line))
                elif typeOfKeyRing == 'pub':
                    self.pub_keyring.append(PublicRing(*line))

    def add_to_keyring(self, typeOfKeyRing, attributes):
        if typeOfKeyRing == 'priv':
            self.priv_keyring.append(PrivateRing(*attributes))
        else:
            self.pub_keyring.append(PublicRing(*attributes))

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
