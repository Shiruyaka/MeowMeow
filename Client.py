# -*- coding: utf-8 -*-

from Crypto.PublicKey import RSA
from Crypto import Random
from time import gmtime, strftime
import Database

class Client():
    def __init__(self):
      self.db = Database.Database()
      self.id = 1

    def generate_new_pair_key(self):
        random_generator = Random.new().read
        pair_key = RSA.generate(2048, random_generator)

        pub_key_val = pair_key.publickey().exportKey(format='PEM')
        pub_key_id = pub_key_val.split('-----')[2].lstrip().rstrip()
        pub_key_id = pub_key_id[-8:].replace('\n', '')
        data = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        self.db.add_key(pub_key_id, self.id, pub_key_val, data)
