from tkinter import filedialog
from tkinter import *

class Interface(Frame):

    def __init__(self, fenetre, **kwargs):
        Frame.__init__(self, fenetre, width=768, height=576, **kwargs)
        self.pack(fill=BOTH)

        self.panel = PanedWindow()
        self.panel.config(bd=15, relief=RIDGE)
        self.panel.pack(side=TOP)

        self.message = Label(self.panel, text="Sélectionnez le répértoire source:")
        self.message.grid(row=0, column=0)

        self.T = Entry(self.panel)
        self.T.grid(row=0, column=1)

        self.bouton_browse = Button(self.panel, text="Browse", fg="red", command=self.browse)
        self.bouton_browse.grid(row=0, column=2)

        self.bouton_cliquer = Button(self, text="Start", fg="red")
        self.bouton_cliquer.pack()

        self.bouton_quitter = Button(self, text="Quitter", command=self.quit)
        self.bouton_quitter.pack()


    def browse(self):
        self.directory = filedialog.askdirectory()
        self.T.delete(0, END)
        self.T.insert(END, self.directory)