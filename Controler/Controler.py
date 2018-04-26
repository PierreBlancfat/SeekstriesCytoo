from View.View import *
from Model.SegmentationGabor import *
from Model.Model import *

class Controler():

    def __init__(self):
        frame = Tk()
        Label(frame, text="Hello World") #test
        self.model = Model("a", "b")
        self.interface = Interface(frame, self)
        self.interface.mainloop()


    def testEntourage(self):
        image = Image.open('../Data/training_masks/Stries_C2  (6)_p.tif')
        s = SegmentationGabor(image)
        matrix = s.conversionBinaire(image)
        areas = self.model.getCoordStriedArea(matrix)

if __name__ == '__main__':
    Controler()
