# -*- coding: utf-8 -*-

from Crypto.PublicKey import RSA
from Crypto import Random
from time import gmtime, strftime
from collections import namedtuple
import Database
import hashlib
import Utils

PrivateRing = namedtuple('PrivateRing', 'timestamp key_id pub_key priv_key')

class Client():
    def __init__(self, login, passwd):
        self.db = Database.Database()
        self.id = 1
        self.hash_password = hashlib.sha1(passwd)
        self.login = login
        self.priv_keyring = list()

        print(self.login)


    def generate_new_pair_key(self):
        random_generator = Random.new().read
        pair_key = RSA.generate(2048, random_generator)

        pub_key_val = pair_key.publickey().exportKey(format='PEM')
        pub_key_id = pub_key_val.split('-----')[2].lstrip().rstrip()
        pub_key_id = pub_key_id[-8:].replace('\n', '')

        data = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        self.db.add_key(pub_key_id, self.id, pub_key_val, data)

    def export_priv_keyring(self):
        self.priv_keyring.append(PrivateRing('1','2','3','4'))
        with open('priv_keyring.txt', 'w') as w:
            for key in self.priv_keyring:
                record = ''
                for attr in key:
                    record += attr + '|'
                record = record.rstrip('|')
                w.write(record)

    def import_priv_keyring(self):
        with open('priv_keyring.txt', 'r') as r:
            data = r.readlines()
            for line in data:
                line = line.rstrip()
                line = line.split('|')
                record = PrivateRing(line[0], line[1], line[2], line[3])
                self.priv_keyring.append(record)

    def add_to_priv_keyring(self, time, id, pub, priv):
        self.priv_keyring.append(PrivateRing(time, id, pub, priv))

