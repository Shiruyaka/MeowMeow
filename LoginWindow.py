#!/usr/bin/env python
import Tkinter as tk
import RegisterWindow
import Utils

class LoginWindow(tk.Frame):
    def __init__(self, master=None):

        self.master = master
        self.master.title('MeowMeow')
        self.master.geometry('350x250')
        self.master.resizable(1, 1)
        self.frame = tk.Frame.__init__(self)

        self.grid()
        self.createWidgets()

    def go_to_registration(self, event):
        print 'Nein'
        if hasattr(self, 'register_window') == False:
            self.register_window = tk.Toplevel(self.master)
            self.register_app = RegisterWindow.RegisterWindow(self.register_window)


    def change_text(self, event):
        self.register_lbl.configure(foreground='red')

    def revert_text(self, event):
        self.register_lbl.configure(foreground='blue')

    def createWidgets(self):

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

        self.password_entry = tk.Entry(self)
        self.password_entry.grid()

        self.login_btn = tk.Button(self, text='Login', command=Utils.login)
        self.login_btn.grid()

        self.register_lbl = tk.Label(self, text='Not having an account yet?', foreground='blue')
        self.register_lbl.grid()

        self.register_lbl.bind('<Button-1>',self.go_to_registration)
        self.register_lbl.bind('<Enter>', self.change_text)
        self.register_lbl.bind('<Leave>', self.revert_text)



