#!/usr/bin/env python
import Tkinter as tk

def login():
    print 'Nein'
    pass

class LoginWindow(tk.Frame):
    def __init__(self, master=None):

        mw = tk.Tk()
        mw.title('MeowMeow')
        mw.geometry('350x250')
        mw.resizable(0, 0)

        tk.Frame.__init__(self, master=mw )

        self.grid()
        self.createWidgets()

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

        self.login_btn = tk.Button(self, text='Login', command=login)
        self.login_btn.grid()

        self.register_lbl = tk.Label(self, text='Not having an account yet?', foreground='blue', activeforeground='red')
        self.register_lbl.grid()


app = LoginWindow()
app.mainloop()
