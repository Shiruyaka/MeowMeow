import Tkinter as tk
import os
import sys
import re
import ttk
from Tkinter import *
import tkFont


class application(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}

        for F in (app_one, app_two):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(app_one)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class app_one(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        button = ttk.Button(self, text="Page One", command=lambda: controller.show_frame(app_two))
        button.pack()


class app_two(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.msgText = tk.StringVar()
        button = ttk.Button(self, text="Open", command=self.Child_Window)
        button.pack()

    def Child_Window(self):
        win2 = Toplevel()
        new_element_header = ['1st', '2nd', '3rd', '4th']
        treeScroll = ttk.Scrollbar(win2)
        treeScroll.pack(side=RIGHT, fill=Y)
        tree = ttk.Treeview(win2, columns=new_element_header, show="headings", yscrollcommand=treeScroll)
        tree.heading("1st", text="1st")
        tree.heading("2nd", text="2nd")
        tree.heading("3rd", text="3rd")
        tree.heading("4th", text="4th")
        tree.insert("", 0, text="Line 1", values=("1A", "1b"))
        tree.insert("", 0, text="Line 2", values=("1A", "1b"))
        tree.insert("", 0, text="Line 3", values=("1A", "1b"))
        tree.insert("", 0, text="Line 4", values=("1A", "1b"))
        tree.insert("", 0, text="Line 5", values=("1A", "1b"))
        tree.insert("", 0, text="Line 6", values=("1A", "1b"))
        tree.insert("", 0, text="Line 7", values=("1A", "1b"))

        tree.pack(side=LEFT, fill=BOTH)

        treeScroll.configure(command=tree.yview)
        tree.configure(yscrollcommand=treeScroll.set)


app = application()
app.wm_geometry("420x200")
app.wm_title("Test")
app.mainloop()