import Model.entourage_package as e
from Model import SegmentationGabor
from PIL import Image
from Model.Segmentation import Segmentation
import os
import cv2
import time
import multiprocessing
import threading
import numpy as np

class Model():

    def __init__(self, repSource, repDestination):
        self.repSource = ""
        self.repDestination = ""
        self.mat=[]

    def setRepSource(self, repSource):
        self.repSource = repSource
        print(self.repSource)

    def setRepDestination(self, repDestination):
        self.repDestination = repDestination
        print(self.repDestination)

    def saveEntourage(self, image, maskBinaire):
        return e.dessinerEntourage(image, maskBinaire)
    
  
    def SegmentationUneImage(self,nomImg):
        cheminImage = self.repSource + str(nomImg)
        img = cv2.imread(cheminImage)
        imgSeg = Segmentation.segmenterUneImage(img)
        imgEntouree = self.saveEntourage(img, imgSeg)
        Image.fromarray(imgEntouree).save(self.repDestination + str(time.time()) + nomImg)

    def runSegmentation(self):
        nbCore = multiprocessing.cpu_count()
        it = 0
        p = {}
        nomsImagesPartitionne = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
        nomsImages = os.listdir(self.repSource)
        nbImage = len(nomsImages)
        j = -1
        for i in np.arange(0,nbImage):
            if(i%(nbImage/nbCore) <1):
                j += 1
            nomsImagesPartitionne[j].append(nomsImages[i])
            print(nomsImagesPartitionne)
        print(nomsImagesPartitionne)
        while it < nbCore:
            p[it] = threading.Thread(target=self.multipleImage, args=(nomsImagesPartitionne[it],))
            p[it].start()
            it += 1

    def multipleImage(self,nomsImages):
        for nomImg in nomsImages:  # pour chaque image à segmenter
                self.SegmentationUneImage(nomImg)




