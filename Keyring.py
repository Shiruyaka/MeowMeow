# -*- coding: utf-8 -*-

from collections import namedtuple
import time
import random
from Crypto.PublicKey import RSA

PrivateRing = namedtuple('PrivateRing', 'timestamp key_id pub_key priv_key')
PublicRing  = namedtuple('PublicRing', 'timestamp key_id pub_key owner_trust user_name key_legit')

def import_keyring(typeOfKeyRing):

    ring = list()

    try:
        with open(typeOfKeyRing + '_keyring.txt', 'r') as r:

            data = r.read()
            data = data.rstrip().split('@')

            for line in data:
                if not line:
                    continue
                line = line.rstrip().split('|')

                if typeOfKeyRing == 'priv':
                    ring.append(PrivateRing(*line))
                elif typeOfKeyRing == 'pub':
                    ring.append(PublicRing(*line))
    except IOError:
        new_file = open(typeOfKeyRing + '_keyring.txt', 'w')
        new_file.close()

    return ring


def export_keyring(ring, typeOfKeyRing):

    with open(typeOfKeyRing + '_keyring.txt', 'w') as w:
        for key in ring:
            record = ''
            for attr in key:
                record += attr + '|'

            record = record.rstrip('|')
            record += '@'
            w.write(record)

def add_to_keyring(ring, typeOfKeyRing, attributes):
    if typeOfKeyRing == 'priv':
        ring.append(PrivateRing(*attributes))
    else:
        ring.append(PublicRing(*attributes))

    return ring

######randomly choose key from private keyring to encrypt

def find_pubkey_in_ring(ring, id = None, whose = None):
    if id:
        result = [x.pub_key for x in ring if x.key_id == id]
        if len(result) == 0:
            return None
        else:
            return RSA.importKey(result[0])
    elif whose:
        result = [x.pub_key for x in ring if x.user_name == whose]
        if len(result) == 0:
            return None
        else:
            print len(result)
            ind = random.randint(0, len(result) - 1)
            print ind
            return RSA.importKey(result[ind])

def find_privkey_in_ring(ring, id):
    result = [x.priv_key for x in ring if x.key_id == id]
    if len(result) != 0:
        return RSA.importKey(result[0])
    else:
        return []

def choose_randomly_enc_key(ring):
    ind = random.randint(0,len(ring) - 1)
    return RSA.importKey(ring[ind].priv_key), ring[ind].key_id


def parse_keys_from_db(data):
    ring = list()

    for i in data:
        tmstmp = time.mktime(i[0].timetuple())
        id = i[1]
        pub_key = str(i[2])
        usr_name = i[3]
        trust = i[4]

        ring.append(PublicRing(tmstmp, id, pub_key , 0, usr_name, trust))

    return ring
