#!/usr/bin/env python
import Tkinter as tk


class RegisterWindow(tk.Frame):
    def __init__(self, master=None):
        mw = tk.Tk()
        mw.master = master
        mw.title('MeowMeow')
        mw.geometry('350x250')
        mw.resizable(0, 0)

        tk.Frame.__init__(self, master=mw)
        self.grid()

