# -*- coding: utf-8 -*-
#!/usr/bin/env python

import Tkinter as tk
import ttk as ttk

class RoomFinderWindow(tk.Frame):
    def __init__(self, master):
        self.master = master
        self.master.title('Room creator')
        self.master.geometry('600x490')
        self.master.resizable(0, 0)

        tk.Frame.__init__(self, master=self.master)

        self.rowconfigure(0, weight = 1)
        self.rowconfigure(1, weight = 1)

        self.grid(sticky='nsew')
        self.create_widgets()



    def create_widgets(self):
        self.filter_entry = tk.Entry(master=self)
        self.filter_entry.grid(sticky = 'we', row = 0, column = 0)

        self.type_of_room_value = tk.StringVar()
        self.type_of_room_combobx = ttk.Combobox(master=self, textvariable=self.type_of_room_value)
        self.type_of_room_combobx['values'] = ('Private', 'Public')
        self.type_of_room_combobx.grid(row = 0, column=1, sticky='nsew')

        self.room_lists = tk.Listbox(master=self, width = 70, height = 30)
        self.room_lists.grid(sticky='nsew', columnspan = 2)

