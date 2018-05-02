from tkinter import filedialog
from tkinter import *
from tkinter import ttk
from Model.Segmentation import Segmentation


class Interface(Tk):

    def __init__(self, controler, **kwargs):

        Tk.__init__(self)
        # Frame configurations
        self.controler = controler

        self.winfo_toplevel().title("SeekStries")  # change Title Bar
        self.s = ttk.Style() # Overall style
        self.s.theme_use('clam')

        self.panel = PanedWindow() # Panel for paths
        self.panel.pack(fill="both", expand=True)

        self.panelCheckbox = PanedWindow(orient=VERTICAL) # Panel for checkboxes
        self.panelCheckbox.pack(expand=True, fill=BOTH)

        self.panelCommands = PanedWindow()  #  Panel for main commands
        self.panelCommands.pack(side=BOTTOM, fill="both", expand=True)


        self.s.configure("BW.TLabel", foreground="white", background="#323232") # Create a style for labels

        # Menu
        self.menuBar = Menu(master=self)
        self.filemenu = Menu(self.menuBar, tearoff=0)
        self.filemenu.add_command(label="Hello!")
        self.filemenu.add_command(label="Quit!")
        self.menuBar.add_cascade(label="Fichier", menu=self.filemenu)

        self.helpmenu = Menu(self.menuBar, tearoff=0)
        self.helpmenu.add_command(label="Documentation")
        self.menuBar.add_cascade(label="Aide", menu=self.helpmenu)

        self.config(menu=self.menuBar)

        #ProgressBar
        pb = ttk.Progressbar(self, orient="horizontal", length=200, mode="determinate")
        pb.pack()
        pb.start()
        # CheckBoxes
        self.checkbutton = ttk.Checkbutton(self.panelCheckbox,text='Entourage', style="TCheckbutton", takefocus=0)
        self.checkbutton.grid(row=0, column=0, sticky=W, pady=15,padx=15,)

        self.checkbutton = ttk.Checkbutton(self.panelCheckbox,text='Enregistrer dans un autre dossier les images striées', takefocus=0)
        self.checkbutton.grid(row=1, column=0,padx=15,pady=15)

        # Source repository
        row = 0
        self.labelSource = ttk.Label(self.panel, text="Sélectionnez le répértoire source:")
        self.labelSource.grid(row=0, column=0)

        self.champsRepSource = ttk.Entry(self.panel)
        self.champsRepSource.grid(row=0, column=1)
        self.champsRepSource.insert(END, "../Data/images/")

        self.browseRepSource = ttk.Button(self.panel, text="Browse", command=self.browse)
        self.browseRepSource.grid(row=0, column=2)

        # Dest repository
        self.labelDest = ttk.Label(self.panel, text="Sélectionnez le répértoire dest:")
        self.labelDest.grid(row=1, column=0)

        self.champsRepDest = ttk.Entry(self.panel)
        self.champsRepDest.grid(row=1, column=1)
        self.champsRepDest.insert(END, "../Data/testSegGabor/seg/")

        self.browseRepDest = ttk.Button(self.panel, text="Browse", command=self.browse)
        self.browseRepDest.grid(row=1, column=2)

        # Main commands
        self.bouton_cliquer = ttk.Button(self.panelCommands, text="Start",command=self.cliquer)
        self.bouton_cliquer.grid(row=0, column=0, pady=30,padx=15)

        self.bouton_cliquer = ttk.Button(self.panelCommands, text="Pause",command=self.pause)
        self.bouton_cliquer.grid(row=0, column=1, pady=30,padx=15)

        self.bouton_cliquer = ttk.Button(self.panelCommands, text="Stats", command=self.createWindowStats)
        self.bouton_cliquer.grid(row=0, column=2, pady=30,padx=15)

        self.bouton_quitter = ttk.Button(self.panelCommands, text="Quitter", command=self.quit)
        self.bouton_quitter.grid(row=0, column=3, pady=30,padx=15)


    def browse(self):
        self.directory = filedialog.askdirectory()
        self.T.delete(0, END)
        self.T.insert(END, self.directory)

    def cliquer(self):
        self.controler.giveRepPath(self.champsRepSource.get(), self.champsRepDest.get())
        self.controler.segmentation()

    def pause(self):
        self.controler.testEntourage()

    def createWindowStats(self):
        windowStats = Toplevel(self)
        windowStats.winfo_toplevel().title("Statistiques")  # change Title Bar

        style = ttk.Style() # Global style
        style.configure("BW.TLabel", foreground="white", background="#323232")  # Create a style for TITLES

        ### Title Panel
        windowStatsPanel = PanedWindow(windowStats)
        windowStatsPanel.pack(fill=BOTH, expand=True)
        windowStatsPanel.configure(background='#323232')

        # Affichage des titres
        windowStatsMessage = ttk.Label(windowStatsPanel, text="IMAGES", style="BW.TLabel", justify=CENTER)
        windowStatsMessage.grid(row=0, column=0, sticky=N+S)
        windowStatsMessage = ttk.Label(windowStatsPanel, text="POURCENTAGE DE STRIES", style="BW.TLabel")
        windowStatsMessage.grid(row=0, column=1, sticky=N+S)
        windowStatsMessage = ttk.Label(windowStatsPanel, text="STRIE OU NON?", style="BW.TLabel")
        windowStatsMessage.grid(row=0, column=2, sticky=N+S)
        windowStatsMessage = ttk.Label(windowStatsPanel, text="AFFICHER IMAGE", style="BW.TLabel")
        windowStatsMessage.grid(row=0, column=3, sticky=N+S)

        ### Data Panel
        #windowStatsPanelData = PanedWindow(windowStats)
        #windowStatsPanelData.pack()
        n = 10
        for i in range (n): # Display path
            windowStatsMessage = ttk.Label(windowStatsPanel, text="Stries_C2  (8).TIF")
            windowStatsMessage.grid(row=i+1,column=0, sticky=N+S+E+W)

        for i in range(n): # Display percentages
            windowStatsMessage = ttk.Label(windowStatsPanel, text="90%", anchor="center")
            windowStatsMessage.grid(row=i+1, column=1, sticky=N+S+E+W)
        for i in range(n): # Striations or not ?
            windowStatsMessage = ttk.Label(windowStatsPanel, text="Oui")
            windowStatsMessage.grid(row=i+1, column=2, sticky=N+S+E+W)
        for i in range(n): # Display images
            windowStatsButton= ttk.Button(windowStatsPanel,text="↗")
            windowStatsButton.grid(row=i+1, column=3, sticky=N+S+E+W)

        # Save button
        windowStatsButton = ttk.Button(windowStatsPanel, text="Sauvegarder")
        windowStatsButton.grid(row=11, column=3, sticky=N + S + E + W)




