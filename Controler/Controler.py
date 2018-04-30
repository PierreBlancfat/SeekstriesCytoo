from View.View import *
from Model.Model import *
from tkinter import ttk

class Controler():

    def __init__(self):
        self.model = Model("a", "b")
        self.interface = Interface(self)
        self.interface.configure(background='#323232')
        self.interface.mainloop()

    def segmentation(self):
        self.model.runSegmentation()

    def testEntourage(self):
        print("a faire depuis le Model direcrement")
        #self.model.saveEntourage() call this function in the model object

if __name__ == '__main__':
    Controler()
