import Tkinter as tk
import ttk

class ToggledFrame(tk.Frame):
    def __init__(self, master = None, title ='', row = 0):
        self.master = master
        self.general_frame = tk.Frame(master = self.master)
        self.general_frame.grid(row = row, sticky = tk.N + tk.S + tk.E + tk.W)
        self.show = tk.BooleanVar(False)

        self.create_widgets(title)

    def create_widgets(self, title):
        self.lst_name_label = tk.Label(master = self.general_frame, text= title)
        self.lst_name_label.grid(row = 0, column = 0)
        self.toggle_btn = tk.Checkbutton(master=self.general_frame, variable=self.show, command=self.toggle)
        self.toggle_btn.grid(row = 0, column = 1)

        self.sub_frame = tk.Frame(master=self.general_frame)
        self.item_listbox = tk.Listbox(master=self.sub_frame)


    def toggle(self):
        if(self.show.get()):
            self.sub_frame.grid(sticky = tk.N + tk.S + tk.E + tk.W)
            self.item_listbox.grid(sticky = tk.N + tk.S + tk.E + tk.W)
        else:
            self.item_listbox.grid_forget()
            self.sub_frame.grid_forget()




class UserWindow(tk.Frame):
    def __init__(self, master=None):
        self.master = master
        self.master.title('MeowMeow')
        self.master.geometry('350x450')
        self.master.resizable(0, 0)

        tk.Frame.__init__(self, master=self.master)
        self.grid()

        self.create_widget()

    def show_about_window(self):
        print 'About'

    def create_widget(self):
        top = self.winfo_toplevel()
        self.menu_bar = tk.Menu(top)
        top['menu'] = self.menu_bar

        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label='File', menu=self.file_menu)

        self.security_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label='Security', menu=self.security_menu)

        self.social_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label='Social', menu=self.social_menu)

        self.file_menu.add_command(label='About', command=self.show_about_window)

        self.owned_rooms = ToggledFrame(self.master, title='Your rooms')
        self.friendly_rooms = ToggledFrame(self.master, title ='Friendly rooms', row = 1)

      #  self.owned_rooms.grid()


        #self.tree_top = tk.Toplevel(self.master)
        #self.tree = ttk.Treeview(self.master, selectmode="extended")
        #ysb = ttk.Scrollbar(self.master, command=self.tree.yview, orient=tk.VERTICAL)
        #self.tree.configure(yscrollcommand = ysb)

        #tree.pack(expand=tk.YES, fill=tk.BOTH)
        #id2 = self.tree.insert("", 1, "dir2", text="Dir 2")
        #self.tree.insert(id2, "end", "dir 2", text="sub dir 2", values=("2A", "2B"))

        #self.tree.grid(sticky = tk.N + tk.W + tk.E + tk.S, row = 0)
