import Model.entourage_package as e
from Model.SegmentationGabor import *

class Model():

    def __init__(self, repSource, repDestination):
        self.repSource = repSource
        self.repDestination = repDestination


    def entourage(self):
        image = cv2.imread('../Data/images/Stries_C2  (78).TIF')
        s = SegmentationGabor(image)
        maskBinaire = s.segmentation()
        maskBinaire = s.conversionBinaire(maskBinaire)
        Image.fromarray(maskBinaire*255).show()
        image = e.dessinerEntourage(image, maskBinaire)
        cv2.imshow('entourage', image)


