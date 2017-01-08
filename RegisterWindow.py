# -*- coding: utf-8 -*-
#!/usr/bin/env python

import Tkinter as tk
import socket
from hashlib import sha1
from Crypto.PublicKey import RSA
import Utils
from Keyring import PublicRing, PrivateRing
import Database


class RegisterWindow(tk.Frame):
    def __init__(self, master=None):


        self.master = master
        self.master.title('Create new account')
        self.master.geometry('350x250')
        self.master.resizable(0, 0)
        self.public_keyring = list()
        self.private_kering = list()
        key = RSA.importKey(open('pub_key.pem', 'r'))
        id = Utils.get_key_id(key)

        self.public_keyring.append(PublicRing('', id, key.exportKey(), '', '', ''))

        tk.Frame.__init__(self, master=self.master)

        self.grid()
        self.create_widgets()

    def create_widgets(self):

        top = self.winfo_toplevel()
        top.rowconfigure(0, weight=1)
        top.columnconfigure(0, weight=1)

        self.error_label = tk.Label(self, text="", foreground='red')

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.user_lbl = tk.Label(self, text='Username')
        self.user_lbl.grid(column=0, row=0)

        self.user_entry = tk.Entry(self)
        self.user_entry.grid(column=0, row=1)

        self.passwd_lbl = tk.Label(self, text='Password')
        self.passwd_lbl.grid(column=0, row=2)

        self.passwd_entry = tk.Entry(self, show='*')
        self.passwd_entry.grid(column=0, row=3)

        self.repeat_passwd_lbl = tk.Label(self, text='Repeat password')
        self.repeat_passwd_lbl.grid(column=0, row=4)

        self.repeat_passwd_entry = tk.Entry(self, show='*')
        self.repeat_passwd_entry.grid(column=0, row=5)

        self.first_name = tk.Label(self, text='First Name*')
        self.first_name.grid(column=1, row=0)

        self.first_name_entry = tk.Entry(self)
        self.first_name_entry.grid(column=1, row=1)

        self.second_name = tk.Label(self, text='Second Name*')
        self.second_name.grid(column=1, row=2)

        self.second_name_entry = tk.Entry(self)
        self.second_name_entry.grid(column=1, row=3)

        self.mail = tk.Label(self, text='E-mail*')
        self.mail.grid(column=1, row=4)

        self.mail_entry = tk.Entry(self)
        self.mail_entry.grid(column=1, row=5)

        self.login_btn = tk.Button(self, text='Register')
        self.login_btn.bind('<Button-1>', self.save_in_database)
        self.login_btn.grid(columnspan=2, column=0)

        self.tmp = tk.Label(self, text='*optional')
        self.tmp.place(rely=1.0, relx=1.0, x=0, y=0, anchor='se')

    def save_in_database(self, event):
        print('close')
        if not self.validate_data():

            try:
                self.server_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.server_conn.connect(('localhost', 5000))
            except:
                print 'Connection problem'
                exit(0)

            data, key = Utils.generate_new_pair_key()
            pubkey = key.publickey().exportKey(format='PEM')
            id = Utils.get_key_id(key.publickey())

            self.private_kering.append(PrivateRing(data, id, pubkey, key.exportKey()))

            args = ['REG', ]
            args.append(self.user_entry.get())
            args.append(self.first_name_entry.get())
            args.append(self.second_name_entry.get())
            args.append(self.mail_entry.get())
            args.append(sha1(self.passwd_entry.get()).hexdigest())
            args.append(data)
            args.append(pubkey)

            key_server_pub = RSA.importKey(open('pub_key.pem', 'r').read())
            key_server_id = Utils.get_key_id(key_server_pub)

            msg = Utils.make_msg(args)
            msg = Utils.pgp_enc_msg(key_server_pub,key,msg)
            msg = msg.ljust(8192, '=')
            #print len(msg)
            self.server_conn.send(msg)
            respond = self.server_conn.recv(8192)
            respond = Utils.pgp_dec_msg(respond, self.public_keyring, self.private_kering)


            if respond[1] == 'OK':
                self.error_label.forget()
                with open('priv_keyring.txt', 'w') as file:
                    #PrivateRing = namedtuple('PrivateRing', 'timestamp key_id pub_key priv_key')
                    msg = Utils.make_msg((data, id, pubkey, key.exportKey()))
                    file.write(msg + '@')
                with open('pub_keyring.txt', 'w') as file:
                    msg = Utils.make_msg(('',key_server_id, key_server_pub.exportKey(), Utils.OwnerTrust.always_trusted, 'Server', 1))
                    msg += '@'
                    file.write(msg)

                self.master.destroy()
            else:
                self.error_label.config(text="Nickname is taken!")
                self.error_label.grid(columnspan=2, column=0)


    def validate_data(self):

        show_label = False

        if self.user_entry.get() == '' or self.passwd_entry.get() == '' or self.repeat_passwd_entry.get() == '':
            self.error_label.config(text="Obligatory fileds can't be empty!")
            show_label = True


        elif self.passwd_entry.get() != self.repeat_passwd_entry.get():
            self.error_label.config(text="Passwords are different!")
            show_label = True

        if show_label:
            self.error_label.grid(columnspan=2, column=0)
        else:
            self.error_label.grid_forget()

        return show_label
