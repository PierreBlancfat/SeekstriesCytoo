from tkinter import filedialog
from tkinter import *
from tkinter import ttk
from Model.Segmentation import Segmentation


class Interface(Frame):

    def __init__(self, fenetre, controler, **kwargs):
        Frame.__init__(self, fenetre, width=768, height=576, **kwargs)
        # Frame configurations
        self.controler = controler
        self.pack(fill=BOTH)

        self.panel = PanedWindow()
        self.panel.pack(side=TOP)

        self.winfo_toplevel().title("SeekStries") # change Title Bar
        self.s = ttk.Style()
        self.s.theme_use('clam')

        self.s.configure("BW.TLabel", foreground="white", background="#323232") # Create a style for labels

        # Menu
        self.filemenu = Menu(self.panel, tearoff=0)
        self.filemenu.add_command(label="Open")
        self.filemenu.add_command(label="Save")
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Exit")
        self.filemenu.add_cascade(label="File", menu=self.filemenu)


        #Row 0
        row = 0
        self.message = ttk.Label(self.panel, text="Sélectionnez le répértoire source:")
        self.message.grid(row=0, column=0)

        self.T = ttk.Entry(self.panel)
        self.T.grid(row=0, column=1)

        self.bouton_browse = ttk.Button(self.panel, text="Browse", command=self.browse)
        self.bouton_browse.grid(row=0, column=2)

        #Row 1
        self.message = ttk.Label(self.panel, text="Sélectionnez le répértoire dest:")
        self.message.grid(row=1, column=0)

        self.T = ttk.Entry(self.panel)
        self.T.grid(row=1, column=1)

        self.bouton_browse = ttk.Button(self.panel, text="Browse", command=self.browse)
        self.bouton_browse.grid(row=1, column=2)


        self.bouton_cliquer = ttk.Button(self, text="Start",command=self.cliquer)
        self.bouton_cliquer.pack()

        self.bouton_cliquer = ttk.Button(self, text="YaraBG",command=self.yaraPerformed)
        self.bouton_cliquer.pack()

        self.bouton_quitter = ttk.Button(self, text="Quitter", command=self.quit)
        self.bouton_quitter.pack()


    def browse(self):
        self.directory = filedialog.askdirectory()
        self.T.delete(0, END)
        self.T.insert(END, self.directory)

    def cliquer(self,cheminScr=None,cheminDest=None):
        self.controler.segmentation()

    def yaraPerformed(self):
        self.controler.testEntourage()



