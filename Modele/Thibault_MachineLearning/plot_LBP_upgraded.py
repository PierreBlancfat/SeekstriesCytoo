"""
===============================================
Local Binary Pattern 
===============================================
https://machinelearningmastery.com/tutorial-to-implement-k-nearest-neighbors-in-python-from-scratch/
"""
from __future__ import print_function
import numpy as np
import matplotlib.pyplot as plt
from knn import knn
from image import image
import csv


plt.rcParams['font.size'] = 9



######################################################################


# settings for LBP
radius = 1
n_points = 8 * radius


scall = 1/2
# dimensions d'une image :
hImg = 1024*scall
lImg = 1344*scall
# nombre de rectangles :
nbRecH = int(32*scall)
nbRecL = int(24*scall)
# dimensions d'un rectangle :
hRec = int(hImg/nbRecH)
lRec = int(lImg/nbRecL)

# taille d'un vecteur caractérisant un sous rectangle
vecSize = 28



# image pour tester l'algorithme de machine learning :
nameTest = 'training.tif'
nameTest = 'test.tif'

imageAffichee = image(nameTest, resize = False)
imageTest = image(nameTest)
lbpTest = imageTest.LBP(n_points, radius)

testSet = np.zeros((nbRecH, nbRecL, vecSize+1))
# si testSet[i][j] est une strie, testSetOut[i][j]=1, 0 sinon.
# au départ, on initialise tout à 0.
testSetOut = np.zeros((nbRecH, nbRecL))



'''
===============================================
====== FONCTIONS DE GESTION DE FICHIER : ======
===============================================
'''


def initWriter(filePath) :
    """
    Ouvre un fichier a partir de son chemin "filePath" et cree
    un objet lecteur pour lire dans ce fichier.
    - filePath : le chemin du fichier
    retourne un fichier et son objet transcripteur.
    """
    file = open(filePath, "r", newline='')
    reader = csv.reader(file)
    return (reader, file)

def close(file) :
    """
    Ferme le fichier "file"
    - file : le fichier a fermer
    """
    file.close()

'''
===============================================
===============================================
'''






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
            #print(carac[j][i])



'''
===============================
============= MAIN ============
===============================
'''
	


def main():
    # chemin vers le fichier ou enregistrer la caracterisation :
    filePath = "caracTrainingSet.csv"
    caracterisation(testSet, lbpTest)
    k = 2
    for i in range(nbRecH) :
        for j in range(nbRecL) :
            (reader, file) = initWriter(filePath)
            neighbors = knn.getNeighbors(reader, testSet[i][j], k)
            result = knn.getResponse(neighbors)
            
            if(result==1):print(result)
            
            close(file)
            testSetOut[i][j] = result
            





main()

imageAffichee.colorResult(testSetOut)

viewer = imageAffichee.display()
viewer.show()

'''
colorResult(trainingSetOut, imageTrain)
viewer = ImageViewer(imageTrain)
viewer.show()
'''




