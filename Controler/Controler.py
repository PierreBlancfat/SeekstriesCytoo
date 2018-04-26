from View.View import *
from Model.Model import *

class Controler():

    def __init__(self):
        frame = Tk()
        Label(frame, text="Hello World") #test
        self.model = Model("a", "b")
        self.interface = Interface(frame, self)
        self.interface.mainloop()

    def segmentation(self):
        self.model.runSegmentation()

    def testEntourage(self):
        self.model.entourage()

if __name__ == '__main__':
    Controler()
