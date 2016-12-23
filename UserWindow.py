import Tkinter as tk

class UserWindow(tk.Frame):
    def __init__(self, master = None):

        self.master = master
        self.master.title('MeowMeow')
        self.master.geometry('350x450')
        self.master.resizable(0, 0)

        tk.Frame.__init__(self, master = self.master)
        self.grid()

        self.create_widget()


    def create_widget(self):

        top = self.winfo_toplevel()
        self.menuBar = tk.Menu(top)
        top['menu'] = self.menuBar
        self.subMenu = tk.Menu(self.menuBar)
        self.menuBar.add_cascade(label='Help', menu=self.subMenu)
        self.xyzMenu = tk.Menu(self.menuBar)
        self.menuBar.add_cascade(label='Cos', menu=self.xyzMenu)

        self.subMenu.add_command(label='About')