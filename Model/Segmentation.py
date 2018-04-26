import cv2
import os
from PIL import Image
from Model.SegmentationFibre import SegmentationFibre
from Model.SegmentationGabor import SegmentationGabor
from Model.Entourage import Entourage
import time

class Segmentation:

    def __init__(self,cheminSrc,cheminDest):

        self.cheminSrc = "D:/L3MI/2nd_Annee/Cytoo/StriesTestPetit" # object segmentationFibre
        self.cheminDest = "D:/L3MI/2nd_Annee/Cytoo/testSegGabor/seg/" # object segmenation stries
        self.image = None


    def segmenterUneImage(self,srcImage,):
        srcImage = "D:/L3MI/2nd_Annee/Cytoo/Images_stage - Copie/Stries_C2  (44).tif"
        matImg = cv2.imread(srcImage)
        # segFibre = SegmentationFibre()
        segGabor = SegmentationGabor(matImg)
        #maskFibre = segFibre.Segmenter(matImg) #TODO utiliser maskFibre pour économiser la segmentation des stries
        maskGabor = segGabor.segmentation()
        #imageEntoure = Entourage.dessinerEntourage(matImg,maskGabor)
        return maskGabor

    def segmenterDesImages(self):
        nomsImages = os.listdir(self.cheminSrc)
        for img in nomsImages:  # pour chaque image à segmenter
             cheminImage = str(self.cheminSrc) + "/" + str(img) + ".tif"
             imgEntouree = self.segmenterUneImage(cheminImage)
             Image.fromarray(imgEntouree).save(self.cheminDest+str(time.time())+".tif")


     # def combinerSegmentation(self):



