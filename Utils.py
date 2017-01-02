# -*- coding: utf-8 -*-

from Crypto.PublicKey import RSA
from Crypto import Random
from Crypto.Cipher import PKCS1_OAEP
from time import gmtime, strftime
from Crypto.Cipher import AES
from hashlib import sha1

COLOR_OF_WINDOW = '#99CCFF'
TYPE_OF_ROOM = ['Your rooms', 'Rooms', 'Friends']
IV = '0' * 16

def login():
    pass

def get_key_id(key_file):
    key = key_file.exportKey(format = 'PEM')
    pub_key_id = key.split('-----')[2].lstrip().rstrip()
    pub_key_id = pub_key_id[-8:].replace('\n', '')

    return pub_key_id

def generate_new_pair_key():
    random_generator = Random.new().read
    pair_key = RSA.generate(2048, random_generator)

    #pub_key_val = pair_key.publickey().exportKey(format='PEM')
    #pub_key_id = pub_key_val.split('-----')[2].lstrip().rstrip()
    #pub_key_id = pub_key_id[-8:].replace('\n', '')

    data = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    #self.db.add_key(pub_key_id, self.id, pub_key_val, data)

    return data, pair_key

def pgp_enc_msg(key_dst, key_source, msg):
    id = get_key_id(key_dst)

    rsaencrypt = PKCS1_OAEP.new(key_dst)
    session_key = Random.new().read(16)

    encrypted_sess_key = rsaencrypt.encrypt(session_key)

    signHashAlg = PKCS1_OAEP.new(key_source)
    hashMsg = sha1(msg).hexdigest()
    hashMsg = signHashAlg.encrypt(hashMsg)

    cipher = msg + '|' + hashMsg
    cipher = cipher.ljust(4096, '=')

    aes_alg = AES.new(session_key, AES.MODE_CBC, IV)
    mess_en = aes_alg.encrypt(cipher)

    return id + '|' + mess_en

def make_msg(msg_content):
    msg = ''
    for i in range(len(msg_content) - 1) :
        msg += msg_content[i] + '|'

    msg = msg + msg_content[-1]

    return msg

#data, key= generate_new_pair_key()
#print data
#punkey = key.publickey().exportKey(format='PEM')
#print punkey, data

#file = open('pub_key.pem', 'r')
#key_pub = RSA.importKey(file.read())

#file2 = open('priv_key.pem', 'r')
#key_priv = RSA.importKey(file2.read())

#print make_msg(('Lelak', 'cos', 'Teodezja', '', '', punkey, data))

#msg = 'Lelak|cos|Teodezja|||' + key_pub.exportKey(format='PEM') + strftime("%Y-%m-%d %H:%M:%S", gmtime())

#print len(msg)
#print len(pgp_enc_msg(key_pub, key_priv, msg))

#print key.exportKey(format='PEM')
#print get_key_id(key)
