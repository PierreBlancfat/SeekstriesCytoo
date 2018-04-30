import Model.entourage_package as e
from Model import SegmentationGabor
from PIL import Image
from Model.Segmentation import Segmentation
import os
import cv2
import time

class Model():

    def __init__(self, repSource, repDestination):
        self.repSource = ""
        self.repDestination = ""

    def setRepSource(self, repSource):
        self.repSource = repSource
        print(self.repSource)

    def setRepDestination(self, repDestination):
        self.repDestination = repDestination
        print(self.repDestination)

    def saveEntourage(self, image, maskBinaire):
        return e.dessinerEntourage(image, maskBinaire)

    def runSegmentation(self):
        nomsImages = os.listdir(self.repSource)
        for nomImg in nomsImages:  # pour chaque image à segmenter
             cheminImage = self.repSource  + str(nomImg)
             img = cv2.imread(cheminImage)
             imgSeg,maskfibre = Segmentation.segmenterUneImage(img)
             imgEntouree = self.saveEntourage(img,imgSeg)
             Image.fromarray(imgEntouree).save(self.repDestination+str(time.time())+nomImg)




