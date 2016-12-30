import Tkinter as tk
import ttk as t
import Utils

class ToggledFrame(tk.Frame):
    def __init__(self, master = None, title =''):

        self.master = master

        tk.Frame.__init__(self, master = self.master)

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

        self.grid(sticky = tk.N + tk.W + tk.S + tk.E, column = 0)

        #self.show = tk.BooleanVar(False)
        self.show = False
        self.create_widgets(title)

    def create_widgets(self, title):
        #self.lst_name_label = tk.Label(master = self, text= title)
        #self.lst_name_label.grid(row = 0, column = 0, sticky = tk.N + tk.W + tk.S + tk.E)

        #self.toggle_btn = tk.Checkbutton(master=self, variable=self.show, command=self.toggle)
        #self.toggle_btn.grid(row = 0, column = 1, sticky = tk.N + tk.W + tk.S + tk.E)
        self.button = tk.Button(master=self, text = title)
        self.button.bind('<Button-1>', self.toggle)
        self.button.grid(sticky = tk.N + tk.W + tk.S + tk.E)
        self.sub_frame = tk.Frame(master=self, bg='white')

        self.sub_frame.rowconfigure(0, weight=1)
        self.sub_frame.columnconfigure(0, weight=1)

        self.item_listbox = tk.Listbox(master=self.sub_frame)


    def toggle(self, event):
        self.show = not self.show
        if(self.show == True):
            self.sub_frame.grid(sticky = tk.N + tk.W + tk.S + tk.E)
            self.item_listbox.grid(sticky = tk.W + tk.E + tk.S + tk.N)
        else:
            self.item_listbox.grid_forget()
            self.sub_frame.grid_forget()




class UserWindow(tk.Frame):
    def __init__(self, master=None):
        self.master = master
        self.master.title('MeowMeow')
        self.master.geometry('350x450')
        #self.master.resizable(1, 1)

        tk.Frame.__init__(self, master=self.master, bg = Utils.COLOR_OF_WINDOW)
        #self.columnconfigure(0, weight=1)
        #self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)
        self.grid()

        self.create_widget()

        #self.client = client

    def show_about_window(self):
        print 'About'

    def set_scrollregion(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))


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


        self.canvas = tk.Canvas(self.master, borderwidth=0, background=Utils.COLOR_OF_WINDOW)
        self.vrt_scrollbar = tk.Scrollbar(self.master, orient='vertical', command=self.canvas.yview)
        self.canvas.config(yscrollcommand= self.vrt_scrollbar.set)
        self.canvas.grid(column = 0, row = 0, sticky = tk.N + tk.S + tk.W + tk.E)
        self.vrt_scrollbar.grid(sticky = tk.N + tk.S, column = 1, row = 0)

        self.rooms_frame = tk.Frame(self.canvas)


        self.canvas.create_window((0, 0), window=self.rooms_frame, anchor='nw', width = 350, tags ='self.rooms_frame')
        self.rooms_frame.bind('<Configure>', self.set_scrollregion)
        self.rooms_frame.grid(sticky = tk.N + tk.S + tk.W + tk.E)


        self.owned_rooms = ToggledFrame(self.rooms_frame, title='Your rooms')
        self.friendly_rooms = ToggledFrame(self.rooms_frame, title ='Friendly rooms')
        self.friends = ToggledFrame(self.rooms_frame, title='Friends')
