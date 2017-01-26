# -*- coding: utf-8 -*-

import mysql.connector
import hashlib
import Keyring
import Room

class Database():

    __shared_state = {}

    def __init__(self):
        self.__dict__ = self.__shared_state
        try:
            self.connector = mysql.connector.connect(user='root', password='#OlciaKocia01', host='localhost', database='MeowMeowDb', port='3306')
        except Exception as e:
            print 'Cos sie popsulo'
            exit()

    def add_user(self, Nick, FirstName, SecondName, Password, Mail):

        #pass_hash = hashlib.sha1(Password).hexdigest()
        cursor = self.connector.cursor()
        cursor.callproc('Insert_NewUser', (Nick, FirstName, SecondName, Mail, Password))

        id = None

        for i in cursor.stored_results():
            id = i.fetchall()

        self.connector.commit()
        cursor.close()

        return (id[0])[0]

    def add_key(self, KeyId, UsrId, PubKey, CreateTime):

        cursor = self.connector.cursor()
        cursor.callproc('Insert_Pubkey', (KeyId, UsrId, PubKey, CreateTime))
        self.connector.commit()
        cursor.close()

    def verify(self, Nick, Password):
        person_data = None
        cursor = self.connector.cursor()
        cursor.callproc('Authentication', [Nick, Password])

        for i in cursor.stored_results():
            person_data = i.fetchall()

        self.connector.commit()
        cursor.close()

        if len(person_data) > 0:
            return list(person_data[0])
        else: return list()


    def get_user_info(self, IdUsr):
        person_data = None

        cursor = self.connector.cursor()
        cursor.callproc('GetUserInfo',[IdUsr])

        for i in cursor.stored_results():
            person_data = i.fetchall()

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

    def get_keys_of_users(self):
        result = None
        cursor = self.connector.cursor()
        cursor.callproc('GetPublicKeys',())

        for i in cursor.stored_results():
            result = i.fetchall()

        result = Keyring.parse_keys_from_db(result)

        self.connector.commit()
        cursor.close()

        return result

    def create_room(self, RoomName, RoomDesc, RoomMaster, RoomMaxOnline, RoomKind):
        id = None
        cursor = self.connector.cursor()
        cmd = 'SELECT CreateRoom(%s,%s,%s,%s,%s)'
        cursor.execute(cmd, (RoomName, RoomDesc, RoomMaster, RoomMaxOnline, RoomKind))
        id = (cursor.fetchall()[0])[0]
        cursor.callproc('InsertParticipant', (id, RoomMaster))
        self.connector.commit()
        cursor.close()

        return id

    def get_all_rooms(self):
        rooms = None
        cursor = self.connector.cursor()
        cursor.callproc('GetRooms', ())

        for i in cursor.stored_results():
            rooms = i.fetchall()

        self.connector.commit()
        cursor.close()

        return Room.parse_rooms_from_db(rooms)

    def get_room_participants(self, id):
        usr_lst = list()
        respond = None
        cursor = self.connector.cursor()
        cursor.callproc('GetParticipants', (id, ))

        for i in cursor.stored_results():
            respond = i.fetchall()

        self.connector.commit()
        cursor.close()

        if len(respond) > 0:
            for i in respond:
                usr_lst.append(i[0])

        return usr_lst