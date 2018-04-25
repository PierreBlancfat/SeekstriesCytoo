from Model.Area import *
from numpy import *

class Model():

    def __init__(self, repSource, repDestination):
        self.repSource = repSource
        self.repDestination = repDestination


    ############################
    # PARTIE VINCENT (à enlever)
    ############################
    #return the next direction by clockwise
    def next(self, direction):
        #right return down
        if(direction[0] == 1 and direction[1] == 0):
            x = 0
            y = 1
        #down return left
        elif(direction[0] == 0 and direction[1]== 1):
            x = -1
            y = 0
        #left return up
        elif(direction[0] == -1 and direction[1] == 0):
            x = 0
            y = -1
        #up return right
        elif(direction[0] == 0 and direction[1]== -1):
            x = 1
            y = 0
        return [x, y]

    #return the next border point and the next primary direction to check
    def movment(self, matrix, x, y, dx, dy):
        #first direction is in the area
        if(matrix[y+dy][x+dx][0]==1):
            x += dx
            y += dy
            [dx, dy] = self.next(self.next(self.next([dx, dy])))
        #second direction is in the area
        elif(matrix[y+self.next([dx, dy])[1]][x+self.next([dx, dy])[0]][0]==1):
            x+= self.next([dx, dy])[0]
            y+= self.next([dx, dy])[1]
        #third direction is in the area
        elif(matrix[y+self.next(self.next([dx, dy]))[1]][x+self.next(self.next([dx, dy]))[0]][0]==1):
            x+= self.next(self.next([dx, dy]))[0]
            y+= self.next(self.next([dx, dy]))[1]
            [dx, dy]=self.next([dx, dy])
        #fourth direction is in the area
        elif(matrix[y+self.next(self.next(self.next([dx, dy])))[1]][x+self.next(self.next(self.next([dx, dy])))[0]][0]==1):
            x+= self.next(self.next(self.next([dx, dy])))[0]
            y+= self.next(self.next(self.next([dx, dy])))[1]
            [dx, dy] = self.next(self.next([dx, dy]))
        #particaular case: pixel alone in the area
        else:
            [dx, dy] = [0, 0]

        #return [newt border point, next primary direction]
        return [[x, y], [dx, dy]]

    # find the first not null pixel of the image/matrix
    def seekPixel(self, matrix, i, j):
        while i < len(matrix) and j < len(matrix[0]) and (matrix[i][j][0] != 1 or not self.leftHighPixel(matrix, i, j)):
            j += 1
            if(j == len(matrix[0])):
                i += 1
                j=0

        if (i != len(matrix) and j != len(matrix[0])):
            k=0
            while k<len(Area.border) and [i, j]!=Area.border[k]:
                k+=1

            if k!=len(Area.border):
                return [-1, -1]

        return [i, j]

    # make a matrix with a empty row and column around the main matrix
    def rebuildMatrix (self, matrixBase):
        matrix = zeros([len(matrixBase)+2, len(matrixBase[0])+2, 2])

        for i in range(0, len(matrixBase)):
            for j in range(0, len(matrixBase[0])):
                matrix[i+1][j+1][0] = matrixBase[i][j][0]
        return matrix


    def leftHighPixel (self, matrix, i, j):
        return matrix[i-1][j][0]==0 and matrix[i][j-1][0]==0


    # seeking the border of a stries begging at position i,j in main matrix
    def seekBorderStries (self, matrix, i, j):
        if (i < len(matrix)) :
            # point and direction initialisation
            initialPoint = [j, i]
            currentPoint = [j, i]
            primaryDirection = [1, 0]  # right

            # initialise the area with the first not null point
            currentArea = Area(j, i, j, i)

            # get the first next border point
            [currentPoint, primaryDirection] = self.movment(matrix, currentPoint[0], currentPoint[1], primaryDirection[0], primaryDirection[1])
            if self.leftHighPixel(matrix, currentPoint[1], currentPoint[0]):
                Area.border.append(currentPoint)  # check next pixel is a top left pixel of the stries

            # expend the area if the new point is out of the actual area
            currentArea.expend(currentPoint[0], currentPoint[1])

            #browse every border point next by next
            while initialPoint != currentPoint and (currentPoint[0]!=0 or currentPoint[1]!=0):
                # get the first next border point
                [currentPoint, primaryDirection] = self.movment(matrix, currentPoint[0], currentPoint[1], primaryDirection[0], primaryDirection[1])
                if self.leftHighPixel(matrix, currentPoint[1], currentPoint[0]):
                    Area.border.append(currentPoint)  # check next pixel is a top left pixel of the stries
                # expend the area if the new point is out of the actual area
                currentArea.expend(currentPoint[0], currentPoint[1])

            #replace the area cause of the use of rebuildMatrix
            currentArea.move(-1, -1)
            return currentArea
        return None

    # return the list of all areas
    def getCoordStriedArea(self, matrixBase):
        matrix = self.rebuildMatrix(matrixBase)
        areas = []

        coordonneInit = [0, 0]
        coordonneNext = coordonneInit

        print(len(matrix))
        print(len(matrix[0]))
        while coordonneInit[0]<len(matrix) and coordonneInit[1]<len(matrix[0]):

            coordonneNext = self.seekPixel(matrix, coordonneInit[0], coordonneInit[1])
            print("i :" + str(coordonneNext[0]))
            print("j : " + str(coordonneNext[1]))
            if coordonneNext != [-1, -1]:
                coordonneInit = coordonneNext
                area = self.seekBorderStries(matrix, coordonneInit[0], coordonneInit[1])
                if area != None:
                    k=0
                    while k<len(areas) and not area.equals(areas[k]):
                        k+=1
                    if k==len(areas):
                        print("yoo")
                        areas.append(area)
                    else:
                        print("yaa")

            if(coordonneInit[1]+1==len(matrix[0]) and coordonneInit[0]+1<len(matrix)):
                coordonneInit[1] = 0
                coordonneInit[0] = coordonneInit[0]+1
            else:
                coordonneInit[1] = coordonneInit[1]+1

        return areas
