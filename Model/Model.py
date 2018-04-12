from Model.Area import *


class Model():

    def __init__(self, repSource, repDestination):
        self.repSource = repSource
        self.repDestination = repDestination

    def next(self, direction):
        if(direction==[0,1]):
            return [1,0]
        elif(direction==[1,0]):
            return[0,-1]
        elif(direction==[0,-1]):
            return [-1,0]
        elif(direction==[-1,0]):
            return [0,1]
        else:
            print("TA RACE")

    def getCoordStriedArea(self, matrix):
        areas = []
        #tabPixelContour =[][]
        i=0
        j=0
        while i < len(matrix) and j < len(matrix[0]) and matrix[i][j][0] != 1:
            j=0
            while j < len(matrix[0]) and matrix[i][j][0] != 1:
                j += 1
            i += 1

        if(i < len(matrix)):
            initialPoint = [i, j]
            currentPoint = [i, j]
            #tabPixelContour[i][j]=1
            primaryDirection = [0, 1]

            """
            while initialPoint!=currentPoint:
                if(matrix[i][j-1][0]==1):
                    currentPoint=[i,j-1]
                    tabPixelContour[i][j-1][0]=1
                elif(matrix[i+1][j][0]==1):
                    currentPoint=[i+1,j]
                    tabPixelContour[i+1][j][0]=1
                elif(matrix[i][j+1][0]==1):
                    currentPoint=[i,j+1]
                    tabPixelContour[i+1][j][0]=1
                    tabPixelContour[i+1][j+1][0]=1
                elif(matrix[i-1][j][0]==1):
                    currentPoint=[i-1,j]
                    tabPixelContour[i+1][j][0]=1
                    tabPixelContour[i+1][j+1][0]=1
                    tabPixelContour[i][j+1][0]=1
                else:
                    currentPoint=[i,j]
            """

            while initialPoint != currentPoint:
                if(matrix[currentPoint[0]+primaryDirection[0]][currentPoint[1]+primaryDirection[1]]==1):
                    currentPoint[0]=currentPoint[0]+primaryDirection[0]
                    currentPoint[1]=currentPoint[1]+primaryDirection[1]
                    primaryDirection=next(next(next(primaryDirection)))
                elif(matrix[currentPoint[0]+next(primaryDirection)[0]][currentPoint[1]+next(primaryDirection)[1]]==1):
                    currentPoint[0]=currentPoint[0]+primaryDirection[0]
                    currentPoint[1]=currentPoint[1]+primaryDirection[1]
                elif(matrix[currentPoint[0]+next(next(primaryDirection))[0]][currentPoint[1]+next(next(primaryDirection))[1]]==1):
                    currentPoint[0]=currentPoint[0]+primaryDirection[0]
                    currentPoint[1]=currentPoint[1]+primaryDirection[1]
                    primaryDirection=next(primaryDirection)
                elif(matrix[currentPoint[0]+next(next(next(primaryDirection)))[0]][currentPoint[1]+next(next(next(primaryDirection)))[1]]==1):
                    currentPoint[0]=currentPoint[0]+primaryDirection[0]
                    currentPoint[1]=currentPoint[1]+primaryDirection[1]
                    primaryDirection=next(next(primaryDirection))

        areas.append(Area(1, 2, 3, 4))
        return areas

