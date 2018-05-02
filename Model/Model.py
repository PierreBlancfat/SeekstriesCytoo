import Model.entourage_package as entourage
from PIL import Image
from Model.Segmentation import Segmentation
import os
import cv2
import threading
import multiprocessing
import numpy as np

class Model():

    def __init__(self, repSource, repDestination):
        self.repSource = ""
        self.repDestination = ""
        self.mat={}
        self.cbcbEntourage = 1
        self.otherRep = 1

    def setRepSource(self, repSource):
        self.repSource = repSource
        print(self.repSource)

    def setRepDestination(self, repDestination):
        self.repDestination = repDestination
        print(self.repDestination)

    def saveEntourage(self, image, maskBinaire):
        return entourage.dessinerEntourage(image, maskBinaire)
    
  
    def SegmentationUneImage(self,nomImg):
        cheminImage = self.repSource + str(nomImg)
        img = cv2.imread(cheminImage) #TODO exeption n'est pas une image, chemin faux; pas d'image dans le dossier
        imgSeg,maskFibre = Segmentation.segmenterUneImage(img)
        #Statistique sur les images
        prop = Segmentation.propStries(maskFibre, imgSeg) * 100
        self.mat.update({nomImg:round(prop,1)})
        if self.cbcbEntourage == 1:
            imgEntouree = self.saveEntourage(img, imgSeg)
            Image.fromarray(imgEntouree).save(self.repDestination + nomImg)

    def runSegmentation(self,cbEntourage,otherRep):
        self.cbcbEntourage = cbEntourage
        self.otherRep = otherRep
        nbCore = multiprocessing.cpu_count()
        it = 0
        p = {}
        nomsImagesPartitionne = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
        nomsImages = os.listdir(self.repSource)
        nomsImages = np.sort(nomsImages)
        nomsImages = np.flip(nomsImages, 0)
        print(nomsImages)
        nbImage = len(nomsImages)
        j = -1
        for i in range(nbImage):
            if(i%(nbImage/nbCore) <1):
                j += 1
            nomsImagesPartitionne[j].append(nomsImages[i])
        print(nomsImagesPartitionne)
        while it < nbCore:
            p[it] = threading.Thread(target=self.multipleImage, args=(nomsImagesPartitionne[it],))
            p[it].start()
            it += 1

        it=0
        while it<nbCore: # Wait end threads
            p[it].join()
            print("finished")
            it+=1

        return 0

    def multipleImage(self,nomsImages):
        for nomImg in nomsImages:  # pour chaque image à segmenter
                self.SegmentationUneImage(nomImg)




