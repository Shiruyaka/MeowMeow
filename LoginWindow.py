#!/usr/bin/env python
import Tkinter as tk
import RegisterWindow
import UserWindow
import Database
import Client
import Utils


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
        id_usr = self.db.verify(self.login_entry.get(), self.password_entry.get())

        if id_usr != 0:
            client = Client.Client()
            app =  UserWindow.UserWindow(self.master)
            self.destroy()



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



