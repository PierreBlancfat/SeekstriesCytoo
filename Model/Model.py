import Model.entourage_package as entourage
from PIL import Image
from Model.Segmentation import Segmentation
import os
import cv2
import threading
import multiprocessing
import numpy as np
from Controler import Controler

class Model():

    def __init__(self, repSource, repDestination,controler):
        self.repSource = ""
        self.repDestination = ""
        self.mat={}
        self.cbEntourage = 1
        self.otherRep = 1
        self.nbThreadFini = 0
        self.nbTheadLance = 0
        self.controler = controler

    def setRepSource(self, repSource):
        self.repSource = self.normalizePath(repSource)
        print(self.repSource)
    def setRepDestination(self, repDestination):
        self.repDestination =self.normalizePath(repDestination)
        if not os.path.exists(self.repDestination+'Strie/'):
            os.makedirs(self.repDestination+'Strie/')
        self.repDestinationStrie = self.repDestination+'Strie/'
        if not os.path.exists(self.repDestination+'nonStrie/'):
            os.makedirs(self.repDestination+'nonStrie/')
        self.repDestinationNonStrie = self.repDestination+'nonStrie/'
        print(self.repDestinationStrie)
        print(self.repDestinationNonStrie)

    def saveEntourage(self, image, maskBinaire):
        return entourage.dessinerEntourage(image, maskBinaire)
    
  
    def SegmentationUneImage(self,nomImg):
        cheminImage = self.repSource + str(nomImg)
        img = cv2.imread(cheminImage)
        imgSeg,maskFibre = Segmentation.segmenterUneImage(img)
        #Statistique sur les images
        prop = Segmentation.propStries(maskFibre, imgSeg) * 100
        self.mat.update({nomImg:round(prop,1)})
        print(self.cbEntourage)
        if self.cbEntourage == 1:
            imgEntouree = self.saveEntourage(img, imgSeg)
            if(self.mat[nomImg]>0):
                Image.fromarray(imgEntouree).save(self.repDestinationStrie + nomImg)
            else:
                Image.fromarray(imgEntouree).save(self.repDestinationNonStrie + nomImg)
        else: # No contouring
            if (self.mat[nomImg] > 0):
                Image.fromarray(img).save(self.repDestinationStrie + nomImg)
            else:
                Image.fromarray(img).save(self.repDestinationNonStrie + nomImg)


    def runSegmentation(self,cbEntourage,otherRep):
        self.cbEntourage = cbEntourage.get()
        self.otherRep = otherRep.get()
        nbCore = multiprocessing.cpu_count() - 2
        self.nbTheadLance = nbCore
        it = 0
        p = {}
        nomsImagesPartitionne = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
        nomsImages = os.listdir(self.repSource)
        for nomImage in nomsImages:
            if(os.path.isdir(self.repSource+"/"+nomImage) or not nomImage.lower().endswith(('.tif', '.tiff', '.png', '.jpg', '.jpeg','.bmp'))):
                nomsImages.remove(nomImage)
        nomsImages = np.sort(nomsImages)
        nomsImages = np.flip(nomsImages, 0)
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
        return 0

    def multipleImage(self,nomsImages):
        for nomImg in nomsImages:  # pour chaque image à segmenter
                self.SegmentationUneImage(nomImg)
        self.nbThreadFini += 1
        if self.nbThreadFini ==  self.nbTheadLance:
            self.finDeTraitement()

    def normalizePath(self,s):
        s = s.replace("\\","/")
        if not s.endswith("/"):
            s=s+"/"
        return s

    def finDeTraitement(self):
        self.nbTheadLance = 0
        self.nbThreadFini = 0
        self.controler.stopProgressBar()
        self.controler.deverouilleBoutonStat()




