from Model.Model import *
from View.View import *
from PIL import Image
from Model import EvaluationSegmentation

class Controler():

    def __init__(self):
        frame = Tk()
        self.model = Model("a", "b")

        #Test Vincent Yara entourage
        image = Image.open("../data/images/test.TIF")
        matrix = EvaluationSegmentation.conversionBinaire(image)
        areas = self.model.getCoordStriedArea(matrix)
        for i in range(0,len(areas)):
            print(i)
            print(str(areas[i].xTopLeft) + " " + str(areas[i].yTopLeft) + " " + str(areas[i].xBotRight) + " " + str(areas[i].yBotRight))

        self.interface = Interface(frame)
        self.interface.mainloop()