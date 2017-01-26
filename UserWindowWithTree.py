import Tkinter as tk
import ttk as ttk
import Queue
import RoomCreator
import RoomFinderWindow
import Utils
import ChatWindow



class UserWindowWithTree(tk.Frame):
    def __init__(self, client, user_recv, user_send, user_rooms, master=None):

        self.client = client
        self.usr_recv = user_recv
        self.usr_send = user_send
        self.rooms = user_rooms

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

        for i in self.rooms:
            if i.master == self.client.login:
                self.rooms_tree.insert('My rooms', 'end', text=i.name, values=len(i.online))
            else:
                self.rooms_tree.insert('Rooms', 'end', text=i.name, values=len(i.online))

        self.room_windows = list()
        self.room_apps = list()

    def delete_attr(self):
        self.create_room_window.destroy()
        delattr(self, 'create_room_window')
        delattr(self, 'create_room_app')

    def delete_finder(self):
        self.find_room_window.destroy()
        delattr(self, 'find_room_window')
        delattr(self, 'find_room_app')
        pass

    def go_to_creating_room(self):
        if hasattr(self, 'create_room_window') == False:
            self.create_room_window = tk.Toplevel(self.master)
            self.create_room_app = RoomCreator.RoomCreator(self.create_room_window, self.usr_send, self.usr_recv)
            self.create_room_window.protocol('WM_DELETE_WINDOW', self.delete_attr)
        pass

    def go_to_finder_room(self):
        if hasattr(self, 'find_room_window') == False:
            self.find_room_window = tk.Toplevel(self.master)
            self.find_room_app = RoomFinderWindow.RoomFinderWindow(self.find_room_window, self.rooms, self.usr_send, self.usr_recv )
            self.find_room_window.protocol('WM_DELETE_WINDOW', self.delete_finder)
        pass

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
        self.social_menu.add_command(label='Create room', command = self.go_to_creating_room)
        self.social_menu.add_command(label='Find room', command = self.go_to_finder_room)

        self.file_menu.add_command(label='About')


    def delete_room(self):
        for i in self.room_windows:
            print i

    def choose_room(self, event):
        curitem = self.rooms_tree.focus()
        name_of_room = self.rooms_tree.item(curitem)['text']
        result = [x for x in self.rooms if x.name == name_of_room]
        if not hasattr(self, name_of_room + 'window'):
            self.room_windows.append(tk.Toplevel(self.master))
            self.room_apps.append(ChatWindow.ChatWindow(self.room_windows[-1], result, self.room_windows,self.room_apps))


    def create_rooms_tree(self):

        self.rooms_tree = ttk.Treeview(master=self.master, columns=['Online'], height = 20)
        self.rooms_tree.heading('#0', text='Room')
        self.rooms_tree.heading("Online", text="Online")
        self.rooms_tree.column('Online', width=50)
        self.rooms_tree.column('#0', width=285)

        self.rooms_tree.insert('', 1, Utils.TYPE_OF_ROOM[0], text=Utils.TYPE_OF_ROOM[0])

        self.rooms_tree.insert('', 2, Utils.TYPE_OF_ROOM[1], text=Utils.TYPE_OF_ROOM[1])

        self.rooms_tree.insert('', 3, Utils.TYPE_OF_ROOM[2], text=Utils.TYPE_OF_ROOM[2])


        self.tree_scrollbar = ttk.Scrollbar(master=self.master, orient='vertical')  # , command=self.rooms_tree.yview)
        self.tree_scrollbar.configure(command=self.rooms_tree.yview)
        self.rooms_tree.configure(yscrollcommand=self.tree_scrollbar.set)
        self.tree_scrollbar.grid(sticky=tk.N + tk.S, row=1, column=1)
        self.rooms_tree.bind('<Double-1>', self.choose_room)
        self.rooms_tree.grid(row=1, column=0, sticky=tk.N + tk.S + tk.W + tk.E)

    def create_widgets(self):
        self.create_menu()

        self.usr_info_lbl = tk.Label(master=self.master, text='Zalogowany jako ' + self.client.login)
        self.usr_info_lbl.grid(row = 0, column = 0, columnspan = 2)
        self.create_rooms_tree()
