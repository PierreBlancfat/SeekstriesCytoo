from Model.Area import *


class Model():

    def __init__(self, repSource, repDestination):
        self.repSource = repSource
        self.repDestination = repDestination

    def getCoordStriesArea(self):
        areas = []
        areas.append(Area(1, 2, 3, 4))
        return areas
