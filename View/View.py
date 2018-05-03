from tkinter import filedialog
from tkinter import *
from tkinter import ttk
import os
from PIL import ImageTk, Image
import csv
import numpy as np

class Interface(Tk):
    '''
    Class holding the whole user interface of the application
    '''
    def __init__(self, controler, **kwargs):
        '''
        Initialization of the interface and all its components
        :param controler: to which controler this view is linked (see Model - View - Controller to learn more about it)
        :param kwargs: init arguments (python)
        '''
        Tk.__init__(self)
        # Frame configurations
        self.controler = controler

        self.winfo_toplevel().title("SeekStries")  # change Title Bar
        self.s = ttk.Style() # Overall style
        self.s.theme_use('clam')

        self.panelCheckbox = PanedWindow(orient=VERTICAL) # Panel for checkboxes
        self.panelCheckbox.pack(expand=True, fill=BOTH)

        self.panel = PanedWindow()  #  Panel for paths
        self.panel.pack(fill="both", expand=True)

        self.panelCommands = PanedWindow()  #  Panel for main commands
        self.panelCommands.pack(side=BOTTOM, fill="both", expand=True)


        self.s.configure("BW.TLabel", foreground="white", background="#323232") # Create a style for labels

        # Menu
        self.menuBar = Menu(master=self)
        self.filemenu = Menu(self.menuBar, tearoff=0)
        self.filemenu.add_command(label="Paramètres")
        self.menuBar.add_cascade(label="Fichier", menu=self.filemenu)

        self.helpmenu = Menu(self.menuBar, tearoff=0)
        self.helpmenu.add_command(label="Documentation")
        self.menuBar.add_cascade(label="Aide", menu=self.helpmenu)

        self.config(menu=self.menuBar)

        #ProgressBar
        self.s.configure("TProgressbar", thickness=50)  # Create a style for labels
        self.pb = ttk.Progressbar(self, orient="horizontal", length=200, mode="determinate", style="TProgressbar")
        self.pb.pack(fill=BOTH)

        # CheckBoxes
        self.entourage = IntVar(value=1)
        self.checkbuttonEntourage = ttk.Checkbutton(self.panelCheckbox, text='Entourage', style="TCheckbutton", takefocus=0, variable=self.entourage, command=self.changeCheckboxEntourage)
        self.checkbuttonEntourage.grid(row=1, column=0, sticky=W, pady=15,padx=15,)

        self.otherRep = IntVar(value=1)
        self.checkbuttonOtherRep = ttk.Checkbutton(self.panelCheckbox,text='Enregistrer les images (Dossiers séparés)', takefocus=0, variable = self.otherRep, command=self.changeCheckboxOtherRep)
        self.checkbuttonOtherRep.grid(row=0, column=0,padx=15,pady=15)

        # Source repository
        self.labelSource = ttk.Label(self.panel, text="Sélectionnez le répértoire source:")
        self.labelSource.grid(row=0, column=0, pady=30,padx=15)

        self.champsRepSource = ttk.Entry(self.panel)
        self.champsRepSource.grid(row=0, column=1, pady=30,padx=15)
        self.champsRepSource.insert(END, "../Data/images/")

        self.browseRepSource = ttk.Button(self.panel, text="Browse", command=self.browseRepSrc)
        self.browseRepSource.grid(row=0, column=2)

        # Dest repository
        self.labelDest = ttk.Label(self.panel, text="Sélectionnez le répértoire dest:")
        self.labelDest.grid(row=1, column=0, pady=30,padx=15)

        self.champsRepDest = ttk.Entry(self.panel)
        self.champsRepDest.grid(row=1, column=1, pady=30,padx=15)
        self.champsRepDest.insert(END, "../Data/testSegGabor/seg/")

        self.browseRepDest = ttk.Button(self.panel, text="Browse", command=self.browseRepDest)
        self.browseRepDest.grid(row=1, column=2)

        # Main commands
        self.bouton_cliquer = ttk.Button(self.panelCommands, text="Start",command=self.cliquer)
        self.bouton_cliquer.grid(row=0, column=0, pady=30,padx=15)

        self.bouton_cliquer = ttk.Button(self.panelCommands, text="Pause",command=self.pause)
        self.bouton_cliquer.grid(row=0, column=1, pady=30,padx=15)

        # Stat button, use self.bouton_cliquer.config(state="normal") to reactivate it
        x=0
        y=0
        self.bouton_cliquer = ttk.Button(self.panelCommands, text="Stats", state=DISABLED, command=lambda x=x,y=y : self.createWindowStats(x,y))
        self.bouton_cliquer.grid(row=0, column=2, pady=30,padx=15)

        self.bouton_quitter = ttk.Button(self.panelCommands, text="Quitter", command=self.quit)
        self.bouton_quitter.grid(row=0, column=3, pady=30,padx=15)

    def changeCheckboxEntourage(self):
        '''
        Disable dest reposiory if we uncheck the box "Entourage"
        :return:
        '''
        entourage = self.entourage.get()
        if (entourage == 0):
            self.champsRepDest.configure(state='disabled')
            self.browseRepDest.configure(state='disabled')
        else:
            self.champsRepDest.configure(state='normal')
            self.browseRepDest.configure(state='normal')
    def changeCheckboxOtherRep(self):
        otherRep = self.otherRep.get()
        if(otherRep == 0):
            self.champsRepDest.configure(state='disabled')
            self.browseRepDest.configure(state='disabled')
            self.checkbuttonEntourage.configure(state='disabled')
        else:
            self.champsRepDest.configure(state='normal')
            self.browseRepDest.configure(state='normal')
            self.checkbuttonEntourage.configure(state='normal')


    def browseRepSrc(self):
        '''
        Allows to change the source repository
        :return: none
        '''
        self.directory = filedialog.askdirectory()
        self.champsRepSource.delete(0, END)
        self.champsRepSource.insert(END, self.directory)

    def browseRepDest(self):
        '''
        Allow to change the destination repository
        :return: none
        '''
        self.directory = filedialog.askdirectory()
        self.champsRepDest.delete(0, END)
        self.champsRepDest.insert(END, self.directory)

    def cliquer(self):
        '''
        Launch the program itself
        '''
        self.controler.giveRepPath(self.champsRepSource.get(), self.champsRepDest.get())
        self.controler.segmentation()

    def pause(self):
        '''
        Pause the program during its execution
        '''
        self.displayError("LA BASE VIRALE VPN A ETE MISE A JOUR!")
        print("TODO")

    def changeState(self):
        '''
        Allows to unlock Stats tab after the execution
        '''
        self.bouton_cliquer.config(state="normal")


    def displayImage(self, imageName, strie):
        '''
        Display an image in its own size in a different window (on top level)
        :param imageName: String that contains the imageName
        '''
        windowImage = Toplevel(self.windowStats)
        windowImage.winfo_toplevel().title("Image : " + imageName)  # change Title Bar
        if (strie==0):
            img = Image.open(self.controler.model.repDestinationNonStrie+ imageName)
        else:
            img = Image.open(self.controler.model.repDestinationStrie+ imageName)

        windowImage.geometry(str(np.shape(img)[0]) + "x" + str(np.shape(img)[1]))
        img = ImageTk.PhotoImage(img)
        imageLabel = Label(windowImage, image=img)
        imageLabel.image = img
        imageLabel.pack(side="bottom", fill="both", expand="yes")

    def createWindowStats(self, clear, start):
        '''
        Function linked to the Statistiques Window. It creates a whole new window on top of the main one. With details on the results, etc...
        :param clear: Tells if we need to clean the window first
        :param start: where to start in the list of images
        '''

        if (clear==1): # Clear window
            for widget in self.windowStats.winfo_children():
                widget.destroy()
        else:
            self.windowStats = Toplevel(self)
            self.windowStats.winfo_toplevel().title("Statistiques")  # change Title Bar

        style = ttk.Style() # Global style
        style.configure("BW.TLabel", foreground="white", background="#323232")  # Create a style for TITLES

        ### Title Panel
        windowStatsPanel = PanedWindow(self.windowStats)
        windowStatsPanel.pack(fill=BOTH, expand=True)
        windowStatsPanel.configure(background='#323232')

        # Affichage des titres
        windowStatsMessage = ttk.Label(windowStatsPanel, text="   IMAGES   ", style="BW.TLabel", justify=CENTER)
        windowStatsMessage.grid(row=0, column=0, sticky=N+S)
        windowStatsMessage = ttk.Label(windowStatsPanel, text="   POURCENTAGE DE STRIES   ", style="BW.TLabel")
        windowStatsMessage.grid(row=0, column=1, sticky=N+S)
        windowStatsMessage = ttk.Label(windowStatsPanel, text="   STRIE OU NON?   ", style="BW.TLabel")
        windowStatsMessage.grid(row=0, column=2, sticky=N+S)
        windowStatsMessage = ttk.Label(windowStatsPanel, text="   AFFICHER IMAGE   ", style="BW.TLabel")
        windowStatsMessage.grid(row=0, column=3, sticky=N+S)

        ### Data Panel
        #windowStatsPanelData = PanedWindow(self.windowStats)
        #windowStatsPanelData.pack()
        self.sizePage = 20
        n = len(os.listdir(self.controler.model.repSource))
        nomsImagesSrc = os.listdir(self.controler.model.repSource)
        sortedValues = sorted(self.controler.model.mat)
        list.sort(nomsImagesSrc)
        print(start)
        for i in range (start,start+self.sizePage): # Display path
            if(0<=i and i<n):
                windowStatsMessage = ttk.Label(windowStatsPanel, text=nomsImagesSrc[i])
                windowStatsMessage.grid(row=i+1,column=0, sticky=N+S+E+W)

        for i in range (start,start+self.sizePage): # Display path
            if(0<=i and i<n):
                windowStatsMessage = ttk.Label(windowStatsPanel, text=self.controler.model.mat[sortedValues[i]], anchor="center")
                windowStatsMessage.grid(row=i+1, column=1, sticky=N+S+E+W)
        for i in range (start,start+self.sizePage): # Display path
            if(0<=i and i<n):
                if (self.controler.model.mat[sortedValues[i]]>0):
                    windowStatsMessage = ttk.Label(windowStatsPanel, text="Oui", anchor="center")
                    windowStatsMessage.grid(row=i+1, column=2, sticky=N+S+E+W)
                else:
                    windowStatsMessage = ttk.Label(windowStatsPanel, text="Non", anchor="center")
                    windowStatsMessage.grid(row=i + 1, column=2, sticky=N + S + E + W)

        windowStatsButtons = []
        stop = start
        cptBut=0
        j=0
        for i in range (start,start+self.sizePage): # Display path
            if(0<=i and i<n):
                if (self.controler.model.mat[sortedValues[i]] > 0):
                    j=1
                else:
                    j=0
                windowStatsButtons.append(ttk.Button(windowStatsPanel,text="↗", command=lambda i=i,j=j: self.displayImage(nomsImagesSrc[i], j)))
                windowStatsButtons[cptBut].grid(row=i+1, column=3, sticky=N+S+E+W)
                stop += 1
                cptBut+=1

        if(start+self.sizePage>=n and start-self.sizePage>=0): # no next
            x = 1
            i = 0
            y = start
            while(y>0 and i<self.sizePage):
                y -= 1
                i+=1
            windowStatsPrevious = ttk.Button(windowStatsPanel, text="Précédent", command=lambda x=x,y=y : self.createWindowStats(x,y))
            windowStatsPrevious.grid(row=stop+1, column=1, sticky=N+S+E+W)
        elif(start-self.sizePage<0 and start+self.sizePage<n): # no previous
            x=1
            i=0
            y=start
            while(y<n and i<self.sizePage):
                y += 1
                i+=1
            windowStatsNext = ttk.Button(windowStatsPanel, text="Suivant", command=lambda x=x, y=y: self.createWindowStats(x, y))
            windowStatsNext.grid(row=stop + 1, column=2, sticky=N + S + E + W)
        elif(start+self.sizePage<n and start-self.sizePage>=0):
            x=1
            i = 0
            y = start
            while (y > 0 and i < self.sizePage):
                y -= 1
                i+=1
            windowStatsPrevious = ttk.Button(windowStatsPanel, text="Précédent", command=lambda x=x, y=y: self.createWindowStats(x, y))
            windowStatsPrevious.grid(row=stop + 1, column=1, sticky=N + S + E + W)

            i = 0
            y = start
            while (start < n and i < self.sizePage):
                y += 1
                i+=1
            windowStatsNext = ttk.Button(windowStatsPanel, text="Suivant", command=lambda x=x, y=y: self.createWindowStats(x, y))
            windowStatsNext.grid(row=stop + 1, column=2, sticky=N + S + E + W)

        # Save button
        windowStatsSave = ttk.Button(windowStatsPanel, text="Sauvegarder (*.csv)", command=self.saveCSV)
        windowStatsSave.grid(row=start+self.sizePage, column=3, sticky=N + S + E + W)


    def saveCSV(self):
        '''
        A function that save the results in a CSV file at the root of the program
        '''
        saveDirectory = filedialog.askdirectory()
        with open((saveDirectory + '/Resultats.csv'), 'w') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            n = len(os.listdir(self.controler.model.repSource))
            nomsImagesSrc = os.listdir(self.controler.model.repSource)
            sortedValues = sorted(self.controler.model.mat)
            for i in range(n):
                if (self.controler.model.mat[sortedValues[i]] > 0):
                    strRes = 'Oui'
                else:
                    strRes ='Non'
                spamwriter.writerow([nomsImagesSrc[i], str(self.controler.model.mat[sortedValues[i]]), strRes])


    def displayError(self, message):
        '''
            Display an error in a different window (on top level)
            :param message: String that contains the error message
        '''
        windowError = Toplevel(self)
        windowError.winfo_toplevel().title("Error")
        errorLabel = ttk.Label(windowError, text=message)
        errorLabel.pack(fill="both", expand="yes", pady=50,padx=50)

    def runProgressBar(self):
        self.pb.start()

    def stopProgressBar(self):
        self.pb.stop()