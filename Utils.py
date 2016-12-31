# -*- coding: utf-8 -*-

from Crypto.PublicKey import RSA
from Crypto import Random
from Crypto.Cipher import PKCS1_OAEP

COLOR_OF_WINDOW = '#99CCFF'
TYPE_OF_ROOM = ['Your rooms', 'Rooms', 'Friends']
IV = '0' * 256

def login():
    pass

def get_key_id(key_file):
    key = key_file.exportKey(format = 'PEM')
    pub_key_id = key.split('-----')[2].lstrip().rstrip()
    pub_key_id = pub_key_id[-8:].replace('\n', '')

    return pub_key_id


def pgp_enc_msg(key_file):
    en_msg = None
    id = get_key_id(key_file)

    session_key = Random.new().read(128)
    rsaencrypt = PKCS1_OAEP.new(key_file)


    ciphertext = rsaencrypt.encrypt(session_key)




file = open('pub_key.pem', 'r')
key = RSA.importKey(file.read())
pgp_enc_msg(key)

#print key.exportKey(format='PEM')
#print get_key_id(key)
