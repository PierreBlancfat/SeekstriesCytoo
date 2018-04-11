import cv2
import math
import os
import numpy as np
from PIL import Image
import scipy

def evalUneImage(imgRef,imgTest):
    """
    Evaluation de la qualité d'une segmentation 
    :param imgRef: une matrice binaire
    :param imgTest: une matrice binaire
    :return: recouv : pourcentage de recouvrement
             erreur : pourcentage d'erreur
    """
    nbPixelAtrouver = np.sum(imgRef)
    ok = (imgRef & imgTest)
    nonTest = (abs(imgRef - np.ones(imgRef.shape))).astype(int) # inverse de test
    erreur = nonTest & imgTest
    nbOk = np.sum(abs(ok))
    nbErreur = np.sum(erreur)
    pourcentagePositif =  nbOk/nbPixelAtrouver
    pourcentageNegatif = nbErreur/np.sum(nonTest)
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

def conversionBinaire(img):
     """
     Convertie une image en binaire
     :param srcImageRef: Le chemin de l'image 
     :return: Une matrice binaire de même taille que l'image source. Les 1 représentent le "noir" ( zone positive), le 0 le "blanc" ( zone négative)
     """
     imarray = np.array(img) # image to nparray
     imarray = scipy.sign(imarray)  # binarise
     imarray = np.floor(abs(imarray - np.ones(imarray.shape))) #inversion 1 -> 0, 0-> 1
     imarray = imarray.astype(int)
     return  imarray


#main  test
imgTest = Image.open("D:/L3MI/2nd_Annee/Cytoo/Fibres/Stries_C2  (2)_fibre.tif")
imgTest = np.array(imgTest)
imgTest = conversionBinaire(imgTest)
imaRef = Image.open("D:/L3MI/2nd_Annee/Cytoo/Fibres/Stries_C2  (2)_fibre.tif")
imaRef = np.array(imaRef)
imaRef = conversionBinaire(imaRef)
print(evalUneImage(imgTest,imaRef))