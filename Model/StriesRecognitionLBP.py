"""
===============================================
Local Binary Pattern 
===============================================
https://machinelearningmastery.com/tutorial-to-implement-k-nearest-neighbors-in-python-from-scratch/
"""
from __future__ import print_function
import numpy as np
import matplotlib.pyplot as plt
from Knn import Knn
from Image import Image
import csv
import time

######################################################################




'''
OPTIONS :
'''
num = 77 # numero de l'image a afficher

# a priori, les options suivantes sont correctement calibrees :
nbRectHauteur = 32
nbRectLargeur = 24
scall = 1/2


######################################################################


plt.rcParams['font.size'] = 9

# settings for LBP
radius = 1
n_points = 8 * radius



# dimensions d'une image :
hImg = 1024*scall
lImg = 1344*scall
# nombre de rectangles :
nbRecH = int(nbRectHauteur*scall)
nbRecL = int(nbRectLargeur*scall)
# dimensions d'un rectangle :
hRec = int(hImg/nbRecH)
lRec = int(lImg/nbRecL)

# taille d'un vecteur caractérisant un sous rectangle
vecSize = 18



# image pour tester l'algorithme de machine learning :
nameTest = 'images/Stries_C2  ('+str(num)+').tif'

testSet = np.zeros((nbRecH, nbRecL, vecSize+1))
# si testSet[i][j] est une strie, testSetOut[i][j]=1, 0 sinon.
# au départ, on initialise tout à 0.
testSetOut = np.zeros((nbRecH, nbRecL))

imageAffichee = Image(nameTest, resize = False, nbRecH = nbRecH, nbRecL = nbRecL)
imageTest = Image(nameTest, nbRecH = nbRecH, nbRecL = nbRecL)
lbpTest = imageTest.LBP(n_points, radius)




'''
===============================================
====== FONCTIONS DE GESTION DE FICHIER : ======
===============================================
'''


def initReader(filePath) :
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




from skimage import exposure


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
            subRect = exposure.equalize_hist(subRect)
#            subRect = exposure.adjust_sigmoid(subRect)
#            subRect = exposure.adjust_log(subRect)

            hist = np.histogram(subRect, bins=vecSize)
            # on caracterise le carreau avec son histogramme :
            for k in range(0,vecSize):
                set[j][i][k] = hist[0][k]




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
    debutBoucle = time.time()
    m = 0
    for i in range(nbRecH) :
        for j in range(nbRecL) :
            (reader, file) = initReader(filePath)
#            debutNeighbors = time.time()
            neighbors = Knn.getNeighbors(reader, testSet[i][j], k)
#            print("temps getNeighbors : "+str(time.time()-debutNeighbors))
            result = Knn.getResponse(neighbors)            
            m=m+1
            close(file)
            testSetOut[i][j] = result
    print("temps boucle : "+str(time.time()-debutBoucle))
    print(m)




def segmenterStriesLBP():
    debutMain = time.time()
    main()
    print("temps execution : "+str(time.time()-debutMain))
    return imageAffichee.returnMask(testSetOut, scall)




