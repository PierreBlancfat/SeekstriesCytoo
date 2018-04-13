from Model.Area import *


class Model():

    def __init__(self, repSource, repDestination):
        self.repSource = repSource
        self.repDestination = repDestination

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

    #return the list of all areas
    def getCoordStriedArea(self, matrix):
        areas = []

        #find the first not null pixel of the image/matrix
        i=0
        j=0
        while i < len(matrix) and j < len(matrix[0]) and matrix[i][j][0] != 1:
            j += 1
            if(j == len(matrix[0])):
                i += 1
                j=0

        #check if theree is a not null pixel in the image/matrix
        if(i < len(matrix)):
            #point and direction initialisation
            initialPoint = [j, i]
            currentPoint = [j, i]
            primaryDirection = [1, 0] #right

            #initialise the area whith the first not null point
            currentArea = Area(j, i, j, i)

            #get the first next border point
            [currentPoint, primaryDirection] = self.movment(matrix, currentPoint[0], currentPoint[1], primaryDirection[0], primaryDirection[1])
            #expend the area if the new point is out of the actual area
            currentArea.expend(currentPoint[0], currentPoint[1])

            #browse every border point next by next
            while initialPoint != currentPoint and (currentPoint[0]!=0 or currentPoint[1]!=0):
                #get the first next border point
                [currentPoint, primaryDirection] = self.movment(matrix, currentPoint[0], currentPoint[1], primaryDirection[0], primaryDirection[1])
                #expend the area if the new point is out of the actual area
                currentArea.expend(currentPoint[0], currentPoint[1])

        areas.append(currentArea)
        return areas
