# -*- coding: utf-8 -*-

from Crypto.PublicKey import RSA
from Crypto import Random
import time

class Client():
    def __init__(self):
        print 'jeeeej'

    def generate_new_pair_key(self):
        random_generator = Random.new().read
        pair_key = RSA.generate(2048, random_generator)

        pub_key = pair_key.publickey().exportKey(format='PEM').split('-----')[2]
        pub_key.lstrip()
        pub_key.rstrip()

        key_id = pub_key[-64:].replace('\n', '')
        timestamp = int(time.time())





cl = Client()
cl.generate_new_pair_key()
