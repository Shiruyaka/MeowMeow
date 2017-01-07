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
        with open(typeOfKeyRing + '_keyring.txt', 'w') as w:
            for key in self.priv_keyring:
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
                record = PrivateRing(*line)
                self.priv_keyring.append(record)

    def add_to_priv_keyring(self, time, id, pub, priv):
        self.priv_keyring.append(PrivateRing(time, id, pub, priv))


d = PrivateRing(*['a', 'b', 'c', 'd'])
print d
