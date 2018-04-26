import Model.entourage_package as e
from Model.SegmentationGabor import *

class Model():

    def __init__(self, repSource, repDestination):
        self.repSource = repSource
        self.repDestination = repDestination


    def entourage(self):
        image = Image.open('../Data/training_masks/Stries_C2  (6)_p.tif')
        s = SegmentationGabor(image)
        mask = s.conversionBinaire(image)
        e.dessinerEntourage(image, mask)


