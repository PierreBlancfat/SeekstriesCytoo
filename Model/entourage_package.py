from numpy import *
from Model.Area import *
import cv2
import time

# return the next direction by clockwise
def next(direction):
    # right return down
    if direction[0] == 1 and direction[1] == 0:
        x = 0
        y = 1
    # down return left
    elif direction[0] == 0 and direction[1]== 1:
        x = -1
        y = 0
    # left return up
    elif direction[0] == -1 and direction[1] == 0:
        x = 0
        y = -1
    # up return right
    elif direction[0] == 0 and direction[1]== -1:
        x = 1
        y = 0
    return [x, y]

# return the next border point and the next primary direction to check
def movment(matrix, x, y, dx, dy):
    # first direction is in the area
    if matrix[y+dy][x+dx]==1:
        x += dx
        y += dy
        [dx, dy] = next(next(next([dx, dy])))
    # second direction is in the area
    elif matrix[y+next([dx, dy])[1]][x+next([dx, dy])[0]]==1:
        x+= next([dx, dy])[0]
        y+= next([dx, dy])[1]
    # third direction is in the area
    elif matrix[y+next(next([dx, dy]))[1]][x+next(next([dx, dy]))[0]]==1 :
        x+= next(next([dx, dy]))[0]
        y+= next(next([dx, dy]))[1]
        [dx, dy]=next([dx, dy])
    # fourth direction is in the area
    elif matrix[y+next(next(next([dx, dy])))[1]][x+next(next(next([dx, dy])))[0]]==1:
        x += next(next(next([dx, dy])))[0]
        y += next(next(next([dx, dy])))[1]
        [dx, dy] = next(next([dx, dy]))
    # particular case: pixel alone in the area
    else:
        [dx, dy] = [0, 0]

    # return [newt border point, next primary direction]
    return [[x, y], [dx, dy]]

# find the first not null pixel of the images/matrix
def seekPixel(matrix, i, j):
    lineLength = len(matrix) # taille d'une ligne de la matrice
    colLength = len(matrix[0]) # taille d'une colonne de la matrice
    AreaBorderLength = len(Area.border)
    
    while i < lineLength and j < colLength and (matrix[i][j]!= 1 or not leftHighPixel(matrix, i, j)):
        j += 1
        if j == colLength:
            i += 1
            j=0

    if i != lineLength and j != colLength:
        k = 0
        while k<AreaBorderLength and [i, j] != Area.border[k]:
            k += 1

        if k != AreaBorderLength:
            return [-1, -1]

    return [i, j]

# make a matrix with a empty row and column around the main matrix
def rebuildMatrix (matrixBase):
    matrix = zeros([len(matrixBase)+2, len(matrixBase[0])+2])

    for i in range(0, len(matrixBase)):
        for j in range(0, len(matrixBase[0])):
            matrix[i+1][j+1] = matrixBase[i][j]
    return matrix


def leftHighPixel(matrix, i, j):
    return matrix[i-1][j]==0 and matrix[i][j-1]==0

# seeking the border of a stries begging at position i,j in main matrix
def seekBorderStries (matrix, i, j):
    if i < len(matrix) :
        # point and direction initialisation
        initialPoint = [j, i]
        currentPoint = [j, i]
        primaryDirection = [1, 0]  # right

        # initialise the area with the first not null point
        currentArea = Area(j, i, j, i)

        # get the first next border point
        [currentPoint, primaryDirection] = movment(matrix, currentPoint[0], currentPoint[1], primaryDirection[0], primaryDirection[1])
        if leftHighPixel(matrix, currentPoint[1], currentPoint[0]):
            Area.border.append(currentPoint)  # check next pixel is a top left pixel of the stries

        # expend the area if the new point is out of the actual area
        currentArea.expend(currentPoint[0], currentPoint[1])

        # browse every border point next by next
        while initialPoint != currentPoint and (currentPoint[0]!=0 or currentPoint[1]!=0):
            # get the first next border point
            [currentPoint, primaryDirection] = movment(matrix, currentPoint[0], currentPoint[1], primaryDirection[0], primaryDirection[1])
            if leftHighPixel(matrix, currentPoint[1], currentPoint[0]):
                Area.border.append(currentPoint)  # check next pixel is a top left pixel of the stries
            # expend the area if the new point is out of the actual area
            currentArea.expend(currentPoint[0], currentPoint[1])

        # replace the area cause of the use of rebuildMatrix
        currentArea.move(-1, -1)
        return currentArea
    return None

# return the list of all areas
def getCoordStriedArea(matrixBase):

    matrix = rebuildMatrix(matrixBase)
    areas = []
    coordInit = [0, 0] # coordonnees initiales
    coordNext = coordInit
    lineLength = len(matrix) # taille d'une ligne de la matrice
    colLength = len(matrix[0]) # taille d'une colonne de la matrice

    # on parcours toute la matrice pour trouver les zones a entourer :
    while coordInit[0] < lineLength and coordInit[1] < colLength:
        # on cherche le prochain pixel de la matrice faisant
        # partie d'une zone a entourer :
        coordNext = seekPixel(matrix, coordInit[0], coordInit[1])
        
        # si on a trouve un pixel faisant partie d'une zone a entourer :
        if coordNext != [-1, -1]:
            # on se place sur ce pixel :
            coordInit = coordNext
            # on detecte l'aire de la zone a entourer
            area = seekBorderStries(matrix, coordInit[0], coordInit[1])
            # si cette aire n'est pas nulle :
            if area is not None:
                areasLength = len(areas)
                k = 0
                # on verifie que cette aire n'est pas deja detectee.
                # si elle ne l'est pas, on l'ajoute a la liste des aires detectees :
                while k < areasLength and not area.equals(areas[k]):
                    k += 1
                if k == areasLength:
                    areas.append(area)
        # si on atteint la fin d'une ligne, retour en debut de ligne  :
        if coordInit[1]+1 == colLength and coordInit[0]+1 < lineLength:
            coordInit[1] = 0
            coordInit[0] = coordInit[0]+1
        # sinon, on avance dans la ligne courante :
        else:
            coordInit[1] = coordInit[1]+1

    return areas

def dessinerEntourage(image, mask):
    """
    Dessine l'entourage sur l'image à partir du mask
    :param image: Une image matricielle (niveau de gris)
    :param mask: un masque binaire
    :return:  matrice RGB
    """
    # on recupere les coordonees des zones a entourer :
    areas = getCoordStriedArea(mask)
    # puis on affiche cet entourage sur l'image passee en parametres :
    for i in range(0, len(areas)):
        cv2.rectangle(image, (areas[i].xTopLeft, areas[i].yTopLeft), (areas[i].xBotRight, areas[i].yBotRight), (255, 0, 0), 3)
    # et on retourne cette image :
    return image
