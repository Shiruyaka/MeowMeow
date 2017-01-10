import Tkinter as tk
import ttk as ttk
import Utils


class RoomCreator(tk.Frame):
    def __init__(self, master):
        self.master = master
        self.master.title('Room creator')
        self.master.geometry('250x220')
        self.master.resizable(0, 0)

        tk.Frame.__init__(self, master=self.master)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(4, weight=1)
        self.rowconfigure(5, weight=1)
        self.rowconfigure(6, weight=1)
        self.rowconfigure(7, weight=1)
        self.rowconfigure(8, weight=1)
        self.rowconfigure(9, weight=1)

        self.grid(sticky='nsew', row = 0, column = 0)
        self.create_widgets()



    def create_widgets(self):

        self.room_name_lbl = tk.Label(master=self, text='Name')
        self.room_name_entry = tk.Entry(master=self)
        self.room_name_lbl.grid(column = 1)
        self.room_name_entry.grid(column = 0, columnspan = 3, sticky = 'nsew')

        self.user_lim_lbl = tk.Label(master = self, text='User limit')
        self.user_lim_lbl.grid(column = 1)

        self.user_lim_value = tk.IntVar()
        self.user_lim_combobx = ttk.Combobox(master = self, textvariable=self.user_lim_value)
        self.user_lim_combobx['values'] = (range(26)[1:])
        self.user_lim_combobx.grid(column = 0, columnspan = 3, sticky = 'nsew')

        self.type_of_room_lbl = tk.Label(master = self, text='Type of room')
        self.type_of_room_lbl.grid(column = 1)

        self.type_of_room_value = tk.StringVar()
        self.type_of_room_combobx = ttk.Combobox(master = self, textvariable=self.type_of_room_value)
        self.type_of_room_combobx['values'] = ('Private', 'Public')
        self.type_of_room_combobx.grid(column = 0, columnspan = 3, sticky = 'nsew')

        self.room_desc_lbl = tk.Label(master = self, text='Desc')
        self.room_desc_txt = tk.Text(master=self, height = 3, width = 23)
        self.scrollbar = ttk.Scrollbar(self)
        self.scrollbar.config(command=self.room_desc_txt.yview)
        self.room_desc_txt.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.grid(row=8, column = 3, sticky = 'ns')

        self.room_desc_lbl.grid(row = 7,column = 1)
        self.room_desc_txt.grid(row = 8, column = 0, columnspan = 3, sticky = 'nsew')

        self.create_btn = tk.Button(master=self, text='Create')
        self.create_btn.grid(column=2, row = 9, sticky = 's')

        self.cancel_btn = tk.Button(master=self, text='Cancel')
        self.cancel_btn.grid(column=0, row = 9, sticky = 'w')


root = tk.Tk()
RoomCreator(root)
root.mainloop()
