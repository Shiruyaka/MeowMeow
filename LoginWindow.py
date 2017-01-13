#!/usr/bin/env python
import Tkinter as tk
from Crypto.PublicKey import RSA
import socket
from hashlib import sha1
import RegisterWindow
import UserWindowWithTree
import Database
import Client
import Utils
import Keyring


class LoginWindow(tk.Frame):
    def __init__(self, master=None):

        self.master = master
        self.master.title('Login')
        self.master.geometry('350x250')
        self.master.resizable(1, 1)
        self.frame = tk.Frame.__init__(self)
        self.db = Database.Database()
        self.grid()
        self.create_widgets()

    def delete_attr(self):
        self.register_window.destroy()
        delattr(self, 'register_window')
        delattr(self, 'register_app')
        pass

    def go_to_registration(self, event):

        if hasattr(self, 'register_window') == False:
            self.register_window = tk.Toplevel(self.master)
            self.register_app = RegisterWindow.RegisterWindow(self.register_window)
            self.register_window.protocol('WM_DELETE_WINDOW', self.delete_attr)

        pass

    def go_to_user_window(self, event):

        self.error_lbl.forget()
        self.error_keyring_lbl.forget()

        try:
            self.server_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_conn.connect(('localhost', 5000))
        except:
            print 'Connection problem'
            exit(0)

        ########## sprawdzac czy jest plik z priv keyring
        try:
            public_keyring = Keyring.import_keyring('pub')
            private_keyring = Keyring.import_keyring('priv')
            server_key = RSA.importKey(Keyring.find_pubkey_in_ring(public_keyring, whose='Server'))
            user_key = RSA.importKey(private_keyring[0].priv_key)  # powinno jeszcze id zwracac?
            ##na razie tylko jedna osoba na komputerze

            passh = sha1(self.password_entry.get()).hexdigest()
            msg = Utils.make_msg(('LOG', self.login_entry.get(), passh, Utils.get_key_id(user_key.publickey())))

            # print server_key.exportKey()

            msg = Utils.pgp_enc_msg(server_key, user_key, msg)
            msg.ljust(8192, '=')

            self.server_conn.send(msg)
            respond = self.server_conn.recv(8192)
            content = Utils.pgp_dec_msg(respond, public_keyring, private_keyring)
            print content

            if content[1] == 'OK':
                user_data = list()

                user_data.append(content[2])
                user_data.append(self.login_entry.get())
                user_data.append(self.password_entry.get())
                user_data.append(content[3])
                user_data.append(content[4])
                user_data.append(content[5])

                client = Client.Client(user_data, private_keyring, public_keyring, self.server_conn)
                app = UserWindowWithTree.UserWindowWithTree(client, self.master)
                self.destroy()
            else:
                self.error_lbl.grid()

        except:
            print("File doesn't find")
            self.error_keyring_lbl.grid()






    def change_text(self, event):
        self.register_lbl.configure(foreground='red')

    def revert_text(self, event):
        self.register_lbl.configure(foreground='blue')

    def create_widgets(self):

        top = self.winfo_toplevel()
        top.rowconfigure(0, weight=1)
        top.columnconfigure(0, weight=1)

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.login_lbl = tk.Label(self, text='Login')
        self.login_lbl.grid()

        self.login_entry = tk.Entry(self)
        self.login_entry.grid()

        self.login_lbl = tk.Label(self, text='Password')
        self.login_lbl.grid()

        self.password_entry = tk.Entry(self, show='*')
        self.password_entry.grid()

        self.login_btn = tk.Button(self, text='Login', command=Utils.login)
        self.login_btn.bind('<Button-1>', self.go_to_user_window)
        self.login_btn.grid()

        self.register_lbl = tk.Label(self, text='Not having an account yet?', foreground='blue')
        self.register_lbl.grid()
        self.register_lbl.bind('<Button-1>',self.go_to_registration)
        self.register_lbl.bind('<Enter>', self.change_text)
        self.register_lbl.bind('<Leave>', self.revert_text)

        self.error_lbl = tk.Label(master=self.master, text='Invalid username or password', foreground='red')
        self.error_keyring_lbl = tk.Label(master=self.master, text='You must to sign up', foreground='red')



