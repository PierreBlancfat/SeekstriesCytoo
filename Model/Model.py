import Model.entourage_package as e

class Model():

    def __init__(self, repSource, repDestination):
        self.repSource = repSource
        self.repDestination = repDestination


    # return the list of all areas
    def getCoordStriedArea(self, matrixBase):
        matrix = e.rebuildMatrix(matrixBase)
        areas = []

        coordonneInit = [0, 0]
        coordonneNext = coordonneInit

        while coordonneInit[0] < len(matrix) and coordonneInit[1] < len(matrix[0]):

            coordonneNext = e.seekPixel(matrix, coordonneInit[0], coordonneInit[1])
            if coordonneNext != [-1, -1]:
                coordonneInit = coordonneNext
                area = e.seekBorderStries(matrix, coordonneInit[0], coordonneInit[1])
                if area is not None:
                    k = 0
                    while k < len(areas) and not area.equals(areas[k]):
                        k += 1
                    if k == len(areas):
                        areas.append(area)

            if coordonneInit[1]+1 == len(matrix[0]) and coordonneInit[0]+1 < len(matrix):
                coordonneInit[1] = 0
                coordonneInit[0] = coordonneInit[0]+1
            else:
                coordonneInit[1] = coordonneInit[1]+1

        return areas
