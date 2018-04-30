from tkinter import filedialog
from tkinter import *
from tkinter import ttk
from Model.Segmentation import Segmentation


class Interface(Tk):

    def __init__(self, controler, **kwargs):

        Tk.__init__(self)
        # Frame configurations
        self.controler = controler

        self.panel = PanedWindow()
        self.panel.pack(side=TOP)

        self.winfo_toplevel().title("SeekStries") # change Title Bar
        self.s = ttk.Style()
        self.s.theme_use('clam')
        self.s.configure("BW.TLabel", foreground="white", background="#323232") # Create a style for labels

        # Menu
        self.menuBar = Menu(master=self)
        self.filemenu = Menu(self.menuBar, tearoff=0)
        self.filemenu.add_command(label="Hello!")
        self.filemenu.add_command(label="Quit!")
        self.menuBar.add_cascade(label="File", menu=self.filemenu)
        self.helpmenu = Menu(self.menuBar, tearoff=0)
        self.helpmenu.add_command(label="Hello!")
        self.menuBar.add_cascade(label="File", menu=self.helpmenu)
        self.config(menu=self.menuBar)

        #ProgressBar
        pb = ttk.Progressbar(self, orient="horizontal", length=200, mode="determinate")
        pb.pack()
        pb.start()

        #Row 0
        row = 0
        self.labelSource = ttk.Label(self.panel, text="Sélectionnez le répértoire source:")
        self.labelSource.grid(row=0, column=0)

        self.champsRepSource = ttk.Entry(self.panel)
        self.champsRepSource.grid(row=0, column=1)
        self.champsRepSource.insert(END, "../Data/images/")

        self.browseRepSource = ttk.Button(self.panel, text="Browse", command=self.browse)
        self.browseRepSource.grid(row=0, column=2)

        #Row 1
        self.labelDest = ttk.Label(self.panel, text="Sélectionnez le répértoire dest:")
        self.labelDest.grid(row=1, column=0)

        self.champsRepDest = ttk.Entry(self.panel)
        self.champsRepDest.grid(row=1, column=1)
        self.champsRepDest.insert(END, "../Data/testSegGabor/seg/")

        self.browseRepDest = ttk.Button(self.panel, text="Browse", command=self.browse)
        self.browseRepDest.grid(row=1, column=2)

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

    def cliquer(self):
        self.controler.giveRepPath(self.champsRepSource.get(), self.champsRepDest.get())
        self.controler.segmentation()

    def yaraPerformed(self):
        self.controler.testEntourage()



