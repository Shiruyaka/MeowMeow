# -*- coding: utf-8 -*-
#!/usr/bin/env python

import Tkinter as tk


class ChatWindow(tk.Frame):
    def __init__(self, master, room, room_windows, room_apps):
        self.master = master
        self.master.title('Room')
        self.master.geometry('600x490')
        self.master.resizable(0, 0)

        tk.Frame.__init__(self, master=self.master)

        self.grid(sticky='nsew', row = 0, column = 0)
        self.create_widgets()

        self.room = room
        self.master.protocol('WM_DELETE_WINDOW', self.zabij_sie)
        self.room_windows = room_windows
        self.room_apps = room_apps

        self.chat_txt.config(state=tk.NORMAL)
        self.chat_txt.insert(tk.END, "Nia NIa nniiiii niiaaaaa")
        self.chat_txt.config(state=tk.DISABLED)

    @staticmethod
    def add_new_message(window, content):
        window.chat_txt.config(state=tk.NORMAL)
        window.chat_txt.insert(tk.END, content)
        window.chat_txt.config(state=tk.DISABLED)
        window.chat_txt.grid


    def zabij_sie(self):
        no = None
        for i in range(len(self.room_windows)):
            if self.master == self.room_windows[i]:
                del self.room_windows[i]
                del self.room_apps[i]

        self.master.destroy()

    def create_widgets(self):
        self.online_users = tk.Listbox(self, width=18, height=20)
        self.scrollbar1 = tk.Scrollbar(self)
        self.scrollbar1.config(command=self.online_users.yview)
        self.online_users.config(yscrollcommand=self.scrollbar1.set)

        self.online_users.grid(sticky='nsew', column=3, row=0, rowspan=3)
        self.scrollbar1.grid(sticky = 'ns', column=4, row=0, rowspan=3)

        self.chat_txt = tk.Text(master=self, width=60, height=25)
        self.scrollbar3 = tk.Scrollbar(self)
        self.scrollbar3.config(command=self.chat_txt.yview)
        self.chat_txt.config(state=tk.DISABLED)
        self.chat_txt.config(yscrollcommand=self.scrollbar3.set)

        self.chat_txt.grid(sticky='nsew', row=0, column=0, )
        self.scrollbar3.grid(sticky='ns', column=1, row=0, rowspan=1)

        self.input_user_txt = tk.Text(master=self, width=62, height=8)
        self.input_user_txt.grid(column=0, row=2, rowspan=1, columnspan=2)

root = tk.Tk()
k = ChatWindow(root, None, None, None)
root.mainloop()
