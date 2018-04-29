import Model.entourage_package as e
from Model import SegmentationGabor
from PIL import Image
from Model.Segmentation import Segmentation
import os
import cv2
import time

class Model():

    def __init__(self, repSource, repDestination):
        self.repSource = "../Data/images/" #repSource
        self.repDestination = "../Data/testSegGabor/seg/"#repDestination


    def saveEntourage(self, image, maskBinaire):
        #Save to do for Vincent Yara
        return e.dessinerEntourage(image, maskBinaire)

    def runSegmentation(self):
        nomsImages = os.listdir(self.repSource)
        for nomImg in nomsImages:  # pour chaque image à segmenter
             cheminImage = self.repSource  + str(nomImg)
             img = cv2.imread(cheminImage)
             imgSeg = Segmentation.segmenterUneImage(img)
             imgEntouree = self.saveEntourage(img,imgSeg)
             Image.fromarray(imgEntouree).save(self.repDestination+str(time.time())+nomImg)




