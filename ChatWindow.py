# -*- coding: utf-8 -*-
#!/usr/bin/env python

import Tkinter as tk


class RoomCreator(tk.Frame):
    def __init__(self, master):
        self.master = master
        self.master.title('Room creator')
        self.master.geometry('600x490')
        self.master.resizable(0, 0)

        tk.Frame.__init__(self, master=self.master)

        self.grid(sticky='nsew', row = 0, column = 0)
        self.create_widgets()



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



#
# root = tk.Tk()
# RoomCreator(root)
# root.mainloop()