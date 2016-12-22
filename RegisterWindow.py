#!/usr/bin/env python
import Tkinter as tk


class RegisterWindow(tk.Frame):
    def __init__(self, master=None):

        self.master = master
        self.master.title('Create new account')
        self.master.geometry('350x250')
        self.master.resizable(0, 0)

        tk.Frame.__init__(self, master=self.master)
        self.grid()

