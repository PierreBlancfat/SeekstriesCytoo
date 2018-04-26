from tkinter import filedialog
from tkinter import *
from Model.Segmentation import Segmentation


class Interface(Frame):

    def __init__(self, fenetre, controler, **kwargs):
        Frame.__init__(self, fenetre, width=768, height=576, **kwargs)
        self.controler = controler
        self.pack(fill=BOTH)


        self.panel = PanedWindow()
        self.panel.config(bd=15, relief=RIDGE)
        self.panel.pack(side=TOP)

        #Row 0
        row = 0
        self.message = Label(self.panel, text="Sélectionnez le répértoire source:")
        self.message.grid(row=0, column=0)

        self.T = Entry(self.panel)
        self.T.grid(row=0, column=1)

        self.bouton_browse = Button(self.panel, text="Browse", fg="red", command=self.browse)
        self.bouton_browse.grid(row=0, column=2)

        #Row 1
        self.message = Label(self.panel, text="Sélectionnez le répértoire dest:")
        self.message.grid(row=1, column=0)

        self.T = Entry(self.panel)
        self.T.grid(row=1, column=1)

        self.bouton_browse = Button(self.panel, text="Browse", fg="red", command=self.browse)
        self.bouton_browse.grid(row=1, column=2)


        self.bouton_cliquer = Button(self, text="Start", fg="red",command=self.cliquer)
        self.bouton_cliquer.pack()

        self.bouton_cliquer = Button(self, text="YaraBG", fg="red",command=self.yaraPerformed)
        self.bouton_cliquer.pack()

        self.bouton_quitter = Button(self, text="Quitter", command=self.quit)
        self.bouton_quitter.pack()


    def browse(self):
        self.directory = filedialog.askdirectory()
        self.T.delete(0, END)
        self.T.insert(END, self.directory)

    def cliquer(self,cheminScr=None,cheminDest=None):
        seg = Segmentation(cheminScr,cheminDest)
        seg.segmenterDesImages()

    def yaraPerformed(self):
        self.controler.testEntourage()



