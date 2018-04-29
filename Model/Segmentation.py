import cv2
import os
from PIL import Image
from Model.SegmentationGabor import SegmentationGabor
from Model.SegmentationFibre import SegmentationFibre
import numpy as np

class Segmentation:

    def __init__(self,cheminSrc,cheminDest):

        self.cheminSrc = cheminSrc # object segmentationFibre
        self.cheminDest = cheminDest # object segmenation stries
        self.image = None


    def segmenterUneImage(matImg):
        segFibre = SegmentationFibre(matImg)
        maskFibre = segFibre.segmenter() #TODO utiliser maskFibre pour économiser la segmentation des stries
        segGabor = SegmentationGabor(matImg)
        maskGabor = segGabor.segmentation()
        Image.fromarray(maskFibre*255).show()
        maskGabor = maskGabor & maskFibre.astype(int)
        return maskGabor


