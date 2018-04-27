import Model.entourage_package as e
from Model.SegmentationGabor import *

class Model():

    def __init__(self, repSource, repDestination):
        self.repSource = repSource
        self.repDestination = repDestination


    def saveEntourage(self, image, maskBinaire):
        #Save to do for Vincent Yara
        return e.dessinerEntourage(image, maskBinaire)



