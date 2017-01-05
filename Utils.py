# -*- coding: utf-8 -*-

from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto import Random
from Crypto.Hash import SHA256
from Crypto.Cipher import PKCS1_OAEP, AES
from time import gmtime, strftime
from hashlib import sha1
import base64

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

    signer = PKCS1_v1_5.new(key_source)

    digest = SHA256.new()
    digest.update(msg)

    hashMsg = signer.sign(digest)
   # print len(base64.b64encode(hashMsg))

    cipher = msg + ';' + base64.b64encode(hashMsg) + ';'
    cipher = cipher.ljust(4096, '=')

    aes_alg = AES.new(session_key, AES.MODE_CBC, IV)
    mess_en = aes_alg.encrypt(cipher)

    return base64.b64encode(id) + ';' + base64.b64encode(encrypted_sess_key) + ';' + base64.b64encode(mess_en)

def pgp_dec_msg(key, msg):

    msg.rstrip('=')
    content = msg.split(';')

    key_id = base64.b64decode(content[0])
  #  print key_id

    rsadecrypt = PKCS1_OAEP.new(RSA.importKey(open('priv_key.pem', 'r')))
    sessionkey = rsadecrypt.decrypt(base64.b64decode(content[1]))
    aes = AES.new(sessionkey, AES.MODE_CBC, IV)

    msg_de = aes.decrypt(base64.b64decode(content[2])).split(';')
    msg_de.pop()
  #  print msg_de
  #  print len(msg_de[1].rstrip('='))
    msg_de[1] = base64.b64decode(msg_de[1])
    client_key = msg_de[0].split('|')[-1]
  #  print client_key + " cos"
  #  print msg_de

    veryfier = PKCS1_v1_5.new(RSA.importKey(client_key))
    digest = SHA256.new()
    digest.update(msg_de[0])

    #print veryfier.verify(digest, msg_de[1])

    if veryfier.verify(digest, msg_de[1]):
        print 'Valid'
        msg_de = msg_de[0].split('|')
    else:
        print 'Invalid'
        msg_de = None

    return msg_de


def make_msg(msg_content):
    msg = ''
    for i in range(len(msg_content) - 1) :
        msg += msg_content[i] + '|'

    msg = msg + msg_content[-1]

    return msg
