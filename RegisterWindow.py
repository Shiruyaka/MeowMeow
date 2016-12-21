#!/usr/bin/env python
import Tkinter as tk


class RegisterWindow(tk.Frame):
    def __init__(self, master):

        master.title('MeowMeow')
        master.geometry('350x250')
        master.resizable(0, 0)

        tk.Frame.__init__(self, master=master)

        self.grid()
        self.createWidgets()
