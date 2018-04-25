"""
===============================================
Local Binary Pattern 
===============================================
https://machinelearningmastery.com/tutorial-to-implement-k-nearest-neighbors-in-python-from-scratch/
"""
from __future__ import print_function
import numpy as np
import matplotlib.pyplot as plt
from Model.Knn import Knn
from Model.Image import Image
import csv
from skimage import exposure

######################################################################


class SegmentationLBP:

    def __init__(self, matrixImg):
        '''
        Parametres :
            - matrixImg : une matrice representant l'image.
        '''        


        # a priori, les options suivantes sont correctement calibrees :
        nbRectHauteur = 32
        nbRectLargeur = 24
        self.scall = 1/2


        ######################################################################
        
        
        plt.rcParams['font.size'] = 9
        
        # settings for LBP
        radius = 1
        n_points = 8 * radius



        # dimensions d'une image :
        hImg = 1024*self.scall
        lImg = 1344*self.scall
        # nombre de rectangles :
        self.nbRecH = int(nbRectHauteur*self.scall)
        self.nbRecL = int(nbRectLargeur*self.scall)
        # dimensions d'un rectangle :
        self.hRec = int(hImg/self.nbRecH)
        self.lRec = int(lImg/self.nbRecL)
        
        # taille d'un vecteur caractérisant un sous rectangle
        self.vecSize = 18

        
        self.testSet = np.zeros((self.nbRecH, self.nbRecL, self.vecSize+1))
        # si testSet[i][j] est une strie, testSetOut[i][j]=1, 0 sinon.
        # au départ, on initialise tout à 0.
        self.testSetOut = np.zeros((self.nbRecH, self.nbRecL))
        
        self.imageAffichee = Image(matrix = matrixImg, resize = False, nbRecH = self.nbRecH, nbRecL = self.nbRecL)
        imageTest = Image(matrix = matrixImg, nbRecH = self.nbRecH, nbRecL = self.nbRecL)
        self.lbpTest = imageTest.LBP(n_points, radius)




        '''
        ===============================================
        ====== FONCTIONS DE GESTION DE FICHIER : ======
        ===============================================
        '''
        
        
    def _initReader(self,filePath) :
        """
        Ouvre un fichier a partir de son chemin "filePath" et cree
        un objet lecteur pour lire dans ce fichier.
        - filePath : le chemin du fichier
        retourne un fichier et son objet transcripteur.
        """
        file = open(filePath, "r", newline='')
        reader = csv.reader(file)
        return (reader, file)
        
    def _close(self,file) :
        """
        Ferme le fichier "file"
        - file : le fichier a fermer
        """
        file.close()
    
    '''
    ===============================================
    ===============================================
    '''




        
        
        
    def caracterisation(self, set, lbp):
        """
        Caracterise les sous rectangles de lbp par les histogrammes
        de ces sous rectangles, et place ces caractéristiques dans la
        matrice set.
        """
        for i in range(0,self.nbRecL) :
            for j in range(0,self.nbRecH) :
                h0 = j*self.hRec
                l0 = i*self.lRec
                subRect = lbp[h0:h0+self.hRec, l0:l0+self.lRec]
                subRect = exposure.equalize_hist(subRect)
        #            subRect = exposure.adjust_sigmoid(subRect)
        #            subRect = exposure.adjust_log(subRect)
        
                hist = np.histogram(subRect, bins=self.vecSize)
                # on caracterise le carreau avec son histogramme :
                for k in range(0,self.vecSize):
                    set[j][i][k] = hist[0][k]




        
        
    def segmenterStriesLBP(self):
        # chemin vers le fichier ou enregistrer la caracterisation :
        filePath = "../Data/caracTrainingSet.csv"
        self.caracterisation(self.testSet, self.lbpTest)
        k = 2
        for i in range(self.nbRecH) :
            for j in range(self.nbRecL) :
                (reader, file) = self._initReader(filePath)
                neighbors = Knn.getNeighbors(reader, self.testSet[i][j], k)
                result = Knn.getResponse(neighbors)            
                self._close(file)
                self.testSetOut[i][j] = result
        return self.imageAffichee.returnMask(self.testSetOut, self.scall)






