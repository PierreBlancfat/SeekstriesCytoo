import cv2
import os
from PIL import Image
from Model.segmentationFibre import SegmentationFibre
from Model.SegmentationGabor import SegmentationGabor
from Model.Entourage import Entourage

class Segmentation:

    def __init__(self,cheminSrc,cheminDest):

        self.cheminSrc = cheminSrc # object segmentationFibre
        self.cheminDest = cheminDest # object segmenation stries
        self.image = None


    def segmenterUneImage(self,srcImage,):
        matImg = cv2.imread(srcImage)
        segFibre = SegmentationFibre()
        segGabor = SegmentationGabor()
        #maskFibre = segFibre.Segmenter(matImg) #TODO utiliser maskFibre pour économiser la segmentation des stries
        maskGabor = segGabor.segmentation(matImg)
        imageEntoure = Entourage.dessinerEntourage(matImg,maskGabor)
        return imageEntoure

    def segmenterDesImages(self):
        nomsImages = os.listdir(self.cheminSrc)
        for img in nomsImages:  # pour chaque image à segmenter
             cheminImage = self.cheminSrc + "/" + str(img) + ".tif"
             imgEntouree = self.segmenterUneImage(cheminImage)
             Image.fromarray(imgEntouree).save(self.cheminDest)


