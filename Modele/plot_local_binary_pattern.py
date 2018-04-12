"""
===============================================
Local Binary Pattern 
===============================================
https://machinelearningmastery.com/tutorial-to-implement-k-nearest-neighbors-in-python-from-scratch/
"""
from __future__ import print_function
import numpy as np
import matplotlib.pyplot as plt


METHOD = 'uniform'
plt.rcParams['font.size'] = 9


"""
IL FAUT :
    - terminer caracteriserTrainingSet.py
    - adapter le programme pour utiliser le fichier généré par
    caracteriserTrainingSet.py et utiliser plus de données dans le trainingSet.
    Il ne s'agira alors plus d'une matrice associée à une image mais d'un
    vecteur des caractérisations associé à un vecteur binaire (strié/non strié)
    - agrandir la base de données d'entrainement pour détecter plus précisement.
    - TESTER
"""


######################################################################

from skimage.feature import local_binary_pattern
from skimage import io
import math
import operator 


# settings for LBP
radius = 3
n_points = 8 * radius


# dimensions d'une image :
hImg = 1024
lImg = 1344
# dimensions d'un rectangle :
hRec = int(hImg/32)
lRec = int(lImg/24)
# nombre de rectangles :
nbRecH = int(hImg/hRec)
nbRecL = int(lImg/lRec)

# taille d'un vecteur caractérisant un sous rectangle
vecSize = 28

# image pour tester l'algorithme de machine learning :
nameTest = 'test4.tif'
imageTest = io.imread(nameTest)
lbpTest = local_binary_pattern(imageTest, n_points, radius, METHOD)
testSet = np.zeros((nbRecH, nbRecL, vecSize))
# si testSet[i][j] est une strie, testSetOut[i][j]=1, 0 sinon.
# au départ, on initialise tout à 0.
testSetOut = np.zeros((nbRecH, nbRecL))


# image pour entrainer l'algorithme de machine learning :
nameTrain = 'training.tif'
imageTrain = io.imread(nameTrain)
lbpTrain = local_binary_pattern(imageTrain, n_points, radius, METHOD)
trainingSet = np.zeros((nbRecH, nbRecL, vecSize))
# si trainingSet[i][j] est une strie, trainingSetOut[i][j]=1, 0 sinon.
trainingSetOut = np.zeros((nbRecH, nbRecL))
trainingSetOut[16][1] = 1
for i in range(11,14):
    trainingSetOut[20][i] = 1
for i in range(0,6):
    trainingSetOut[17][i] = 1
for i in range(3,11):
    trainingSetOut[18][i] = 1
for i in range(7,19):
    trainingSetOut[19][i] = 1

'''
# code pour dessiner une grille sur l'image, pour identifier rapidement les
# sous rectangles sur lesquels on travail
from skimage.viewer import ImageViewer
def drawGrid():
    for i in range(0,nbRecH) :
        for j in range(0,lImg) :
            imageTrain[i*hRec][j] = imageTrain.size-1
    for i in range(0,hImg) :
        for j in range(0,nbRecL) :
            imageTrain[i][j*lRec] = imageTrain.size-1
drawGrid()
viewer = ImageViewer(imageTrain)
viewer.show()
'''




from skimage.viewer import ImageViewer
def coloriserResult(setOut, image):
    '''
    code pour coloriser les sous rectangles sriés.
    '''
    for i in range(0,nbRecH) :
        for j in range(0,nbRecL) :
            if(setOut[i][j]==1):
                for k in range(0,hRec):
                    l = np.arange(0, lRec)
                    image[i*hRec+k][j*lRec+l] += 7000

                


def euclideanDistance(u, v):
    '''
    Retourne la distance euclidienne entre le vecteur u et v.
    - u et v deux vecteurs de même taille
    '''
    length = np.size(u)
    distance = 0
    for x in range(length-2):
        distance += pow((u[x] - v[x]), 2)
    return math.sqrt(distance)




def getNeighbors(trainingSet, testInstance, k):
    '''
    Retourne les k voisins les plus proches du vecteur testInstance,
    parmi les vecteurs de trainingSet.
    '''
    distances = []
    for i in range(0,nbRecH) :
        for j in range(0,nbRecL) :
            dist = euclideanDistance(testInstance, trainingSet[i][j])
            distances.append((trainingSet[i][j], dist))
    distances.sort(key=operator.itemgetter(1))
    neighbors = []
    for x in range(k):
        neighbors.append(distances[x][0])
    return neighbors




def caracterisation(set, lbp):
    """
    Caracterise les sous rectangles de lbp par les histogrammes
    de ces sous rectangles, et place ces caractéristiques dans la
    matrice set.
    """
    for i in range(0,nbRecL) :
        for j in range(0,nbRecH) :
            h0 = j*hRec
            l0 = i*lRec
            subRect = lbp[h0:h0+hRec, l0:l0+lRec]
            hist = np.histogram(subRect, bins=vecSize)
            #plt.plot(hist[1][0:25], hist[0][0:25])
            # on caracterise le carreau avec son histogramme :
            for k in range(0,vecSize):
                set[j][i][k] = hist[0][k]
            set[j][i][-2] = j
            set[j][i][-1] = i
            #print(carac[j][i])



def getResponse(neighbors, setOut):
    classVotes = {}
    for x in range(len(neighbors)):
        i = int(neighbors[x][-2])
        j = int(neighbors[x][-1])
        response = setOut[i][j]
        if response in classVotes:
            classVotes[response] += 1
        else:
            classVotes[response] = 1
    sortedVotes = sorted(classVotes.items(), key=operator.itemgetter(1), reverse=True)
    return sortedVotes[0][0]



'''
===============================
============= MAIN ============
===============================
'''
	
def main():
    caracterisation(trainingSet, lbpTrain)
    caracterisation(testSet, lbpTest)
    k = 2
    for i in range(0,nbRecH) :
        for j in range(0,nbRecL) :
            neighbors = getNeighbors(trainingSet, testSet[i][j], k)
            result = getResponse(neighbors, trainingSetOut)
            testSetOut[i][j] = result




main()


coloriserResult(testSetOut, imageTest)

viewer = ImageViewer(imageTest)
viewer.show()

'''
coloriserResult(trainingSetOut, imageTrain)
viewer = ImageViewer(imageTrain)
viewer.show()
'''

