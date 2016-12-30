import Tkinter as tk
import ttk as ttk
import Utils


class UserWindowWithTree(tk.Frame):
    def __init__(self, master=None):

        self.master = master
        self.master.title('MeowMeow')
        self.master.geometry('350x450')
        self.master.resizable(0,0)

        tk.Frame.__init__(self, master = self.master)
        self.grid(sticky = 'nsew')
        self.columnconfigure(0, weight = 1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight = 1)
        self.rowconfigure(1, weight=1)
        self.create_widgets()

    def create_menu(self):
        top = self.winfo_toplevel()
        self.menu_bar = tk.Menu(top)
        top['menu'] = self.menu_bar

        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label='File', menu=self.file_menu)

        self.security_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label='Security', menu=self.security_menu)

        self.social_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label='Social', menu=self.social_menu)
        self.file_menu.add_command(label='About')

    def create_rooms_tree(self):

        self.rooms_tree = ttk.Treeview(master=self.master, columns=['Online'], height = 20)
        self.rooms_tree.heading('#0', text='Room')
        self.rooms_tree.heading("Online", text="Online")
        self.rooms_tree.column('Online', width=50)
        self.rooms_tree.column('#0', width=285)

        self.rooms_tree.insert("", 1, Utils.TYPE_OF_ROOM[0], text=Utils.TYPE_OF_ROOM[0])

        self.rooms_tree.insert('', 2, Utils.TYPE_OF_ROOM[1], text=Utils.TYPE_OF_ROOM[1])

        self.rooms_tree.insert('', 3, Utils.TYPE_OF_ROOM[2], text=Utils.TYPE_OF_ROOM[2])


        self.tree_scrollbar = ttk.Scrollbar(master=self.master, orient='vertical')  # , command=self.rooms_tree.yview)
        self.tree_scrollbar.configure(command=self.rooms_tree.yview)
        self.rooms_tree.configure(yscrollcommand=self.tree_scrollbar.set)
        self.tree_scrollbar.grid(sticky=tk.N + tk.S, row=1, column=1)

        self.rooms_tree.grid(row=1, column=0, sticky=tk.N + tk.S + tk.W + tk.E)

    def create_widgets(self):
        self.create_menu()

        self.usr_info_lbl = tk.Label(master=self.master, text='Zalogowany jako')
        self.usr_info_lbl.grid(row = 0, column = 0, columnspan = 2)
        self.create_rooms_tree()


#root = tk.Tk()
#app = UserWindowWithTree(root)
#root.mainloop()