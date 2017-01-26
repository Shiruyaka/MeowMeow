# -*- coding: utf-8 -*-
#!/usr/bin/env python

import Tkinter as tk
import ttk as ttk
from Crypto.PublicKey import RSA
import Keyring
import Utils

class RoomFinderWindow(tk.Frame):
    def __init__(self, master, user_rooms, user_send, user_recv):

        self.user_rooms = user_rooms
        self.user_send = user_send
        self.user_recv = user_recv

        self.master = master
        self.master.title('Room creator')
        self.master.geometry('600x490')
        self.master.resizable(0, 0)

        tk.Frame.__init__(self, master=self.master)

        self.rowconfigure(0, weight = 1)
        self.rowconfigure(1, weight = 1)

        self.grid(sticky='nsew')
        self.create_widgets()


    def get_list_of_rooms(self, event):
        args = list()
        args.append('LRM')
        args.append(self.type_of_room_combobx.get())

        key_user = RSA.importKey(self.user_send.user.priv_keyring[0].priv_key)
        key_id = Utils.get_key_id(key_user.publickey())
        key_server = RSA.importKey(Keyring.find_pubkey_in_ring(self.user_send.user.pub_keyring, whose='Server'))
        args.append(key_id)


        ############ pomysl o dodanu do funckji znajdujacej klucza od razu wyszukiwanie id refaaaacTORRRRR
        msg = Utils.make_msg(args)
        msg = Utils.pgp_enc_msg(key_server, key_user, msg)
        msg.ljust(8192, '=')

        self.user_send.data.put(msg)


    def create_widgets(self):
        self.filter_entry = tk.Entry(master=self)
        self.filter_entry.grid(sticky = 'we', row = 0, column = 0)

        self.type_of_room_value = tk.StringVar()
        self.type_of_room_combobx = ttk.Combobox(master=self, textvariable=self.type_of_room_value)
        self.type_of_room_combobx['values'] = ('Private', 'Public')
        self.type_of_room_combobx.grid(row = 0, column=1, sticky='nsew')

        self.search_btn = tk.Button(self, text='Search')
        self.search_btn.bind('<Button-1>', self.get_list_of_rooms)
        self.search_btn.grid(row = 0, column = 2, sticky ='nsew')

        self.room_lists = tk.Listbox(master=self, width = 70, height = 30)
        self.room_lists.grid(sticky='nsew', columnspan = 3)

