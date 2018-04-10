import cv2
import math
import os
import numpy as np
from PIL import Image
import scipy
np.set_printoptions(threshold=np.nan)
#ciao bella
def evalUneImage(imgRef,imgTest):
    """
    Evaluation de la qualité d'une segmentation 
    :param imgRef: une matrice binaire
    :param imgTest: une matrice binaire
    :return: recouv : pourcentage de recouvrement
             erreur : pourcentage d'erreur
    """
    faux = imgRef - imgTest #
    vrai = imgTest - imgRef
    nbFaux = math.fsum(faux)
    nbvrai = math.fsum(vrai)
    pourcentagePositif = nbFaux/imgTest.length
    pourcentageNegatif= nbvrai / imgRef.length
    return [pourcentagePositif,pourcentageNegatif]


def evalDesImage(srcRef,masqueTest):
    cheminImagesRef = os.listdir(srcRef)
    #cheminImagesTest = os.listdir(srcTest)
    nbImage = cheminImagesRef.__sizeof__()
    result = np.zeros([nbImage,2])
    for i in range(0,nbImage):
        imageRef = conversionBinaire(cheminImagesRef[i])
        result[i] = evalUneImage(imageRef)
    return result

def conversionBinaire(srcImageRef):
     """
     Convertie une image en binaire
     :param srcImageRef: Le chemin de l'image 
     :return: Une matrice binaire de même taille que l'image source. Les 1 représentent le "noir" ( zone positive), le 0 le "blanc" ( zone négative)
     """
     img = Image.open(srcImageRef)
     img = img.convert('L') # niveau de gris
     imarray = np.array(img) # image to nparray
     imarray = scipy.sign(imarray)  # binarise
     imarray = (imarray -1) * -1 #inverse 0=1 et 1=0
     return  imarray


#main  test
