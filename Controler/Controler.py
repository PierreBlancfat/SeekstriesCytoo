from Model.Model import *
from View.View import *
from PIL import Image
from Model import EvaluationSegmentation

class Controler():

    def __init__(self):
        frame = Tk()
        self.model = Model("a", "b")

        #Test Vincent entourage
        image = Image.open("C:/Users/Vincent/PycharmProjects/SeekstriesCytoo/test.TIF")
        matrix = EvaluationSegmentation.conversionBinaire(image)
        areas = self.model.getCoordStriedArea(matrix)
        print(areas)

        self.interface = Interface(frame)
        self.interface.mainloop()