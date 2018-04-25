from Model.Model import *
from View.View import *
from PIL import Image
from Model.EvaluationSegmentation import EvaluationSegmentation

class Controler():

    def __init__(self):
        frame = Tk()
        self.model = Model("../Data/images/", "./Data/imageEnregistre")

        '''
        #Test Vincent entourage
        image = Image.open("../Data/images/Stries_C2  (8).TIF")
        matrix = EvaluationSegmentation.conversionBinaire(image)
        areas = self.model.getCoordStriedArea(matrix)
        for i in range(0,len(areas)):
            print(i)
            print(str(areas[i].xTopLeft) + " " + str(areas[i].yTopLeft) + " " + str(areas[i].xBotRight) + " " + str(areas[i].yBotRight))
        
        
        self.interface = Interface(frame)
        self.interface.mainloop()
        '''
