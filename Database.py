# -*- coding: utf-8 -*-

import mysql.connector
import hashlib

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

    def get_user_info(self, IdUsr):
        person_data = None

        cursor = self.connector.cursor()
        cursor.callproc('GetUserInfo',[IdUsr])

        for i in cursor.stored_results():
            person_data = i.fetchall()[0]

        self.connector.commit()
        cursor.close()

        return person_data

    def check_nickname(self, Nick):
        cursor = self.connector.cursor()
        cursor.execute('SELECT CheckNick(%s)', (Nick, ))
        result  = cursor.fetchall()
        self.connector.commit()
        cursor.close()

        return result[0][0]


db1 = Database()
db1.check_nickname('Ola')
