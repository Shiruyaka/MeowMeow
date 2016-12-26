# -*- coding: utf-8 -*-

import mysql.connector
import hashlib


#class SingletonDatabase():
#    def __init__(self):

class Database():

    __shared_state = {}

    def __init__(self):
        self.__dict__ = self.__shared_state
        try:
            self.connector = mysql.connector.connect(user='root', password='#OlciaKocia01', host='localhost', database='MeowMeowDb', port='3306')
        except Exception as e:
            print 'Cos sie popsulo'
            exit()

    def add_user(self, Nick, FirstName, SecondName, Password):

        pass_hash = hashlib.sha1(Password).hexdigest()
        cursor = self.connector.cursor()
        cursor.callproc('Insert_NewUser', (Nick, FirstName, SecondName, str(pass_hash)))
        self.connector.commit()
        cursor.close()

    def add_key(self, KeyId, UsrId, PubKey, CreateTime):

        cursor = self.connector.cursor()
        cursor.callproc('Insert_Pubkey', (KeyId, UsrId, PubKey, CreateTime))
        self.connector.commit()
        cursor.close()

    def verify(self, Nick, Password):
        cursor = self.connector.cursor()
        cursor.execute('SELECT Authentication_int(%s, %s)',(Nick, str(hashlib.sha1(Password).hexdigest())))
        result = cursor.fetchall()
        self.connector.commit()
        cursor.close()
        return result[0][0]

    def get_user_info(self, idUsr):
        cursor = self.connector.cursor()
        cursor.execute('CALL GetUserInfo(%d)',(idUsr,), True)
        result = cursor.fetchall()
        self.connector.commit()
        cursor.close()

        print result

db1 = Database()

db1.get_user_info(1)