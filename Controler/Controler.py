from Model.Model import *
from View.View import *
from PIL import Image
from Model import EvaluationSegmentation
import os


class Controler():

    def __init__(self):
        frame = Tk()
        self.model = Model("a", "b")

        #Test Vincent Yara entourage

        image = Image.open('../Data/training_masks/Stries_C2  (6)_p.tif')
        matrix = EvaluationSegmentation.conversionBinaire(image)
        areas = self.model.getCoordStriedArea(matrix)
        for i in range(0,len(areas)):
            print(i)
            print(str(areas[i].xTopLeft) + " " + str(areas[i].yTopLeft) + " " + str(areas[i].xBotRight) + " " + str(areas[i].yBotRight))

        self.interface = Interface(frame)
        self.interface.mainloop()