#!/usr/bin/env python
import Tkinter as tk
import RegisterWindow
import Utils

class LoginWindow(tk.Frame):
    def __init__(self, master=None):

        mw = tk.Tk()
        mw.title('MeowMeow')
        mw.geometry('350x250')
        mw.resizable(0, 0)

        tk.Frame.__init__(self, master=mw)

        self.grid()
        self.createWidgets()

    def go_to_registration(self, event):
        print 'Nein'
        self.register_window = RegisterWindow.RegisterWindow(self)
        self.register_window.mainloop()

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
        self.login_lbl.grid(row = 2, column = 2)

        self.login_entry = tk.Entry(self)
        self.login_entry.grid(row = 3, column = 2)

        self.login_lbl = tk.Label(self, text='Password')
        self.login_lbl.grid(row = 5, column = 2)

        self.password_entry = tk.Entry(self)
        self.password_entry.grid(row = 6, column = 2)

        self.login_btn = tk.Button(self, text='Login', command=Utils.login)
        self.login_btn.grid(row = 7, column = 0)

        self.register_lbl = tk.Label(self, text='Not having an account yet?', foreground='blue', background='orange')
        self.register_lbl.grid(row = 9, column = 0)

        self.register_lbl.bind('<Button-1>',self.go_to_registration)
        self.register_lbl.bind('<Enter>', self.change_text)
        self.register_lbl.bind('<Leave>', self.revert_text)


app = LoginWindow()
app.mainloop()
