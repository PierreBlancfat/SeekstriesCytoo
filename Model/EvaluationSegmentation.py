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
    nbTotal = imgRef.size
    vraiPositif = (imgRef & imgTest)
    inverseRef = inverseMatBin(imgRef)
    fauxPositif = inverseRef & imgTest
    vraiNegatif = imgRef & inverseMatBin(vraiPositif)
    fauxNegatif= inverseMatBin(imgTest | imgRef)
    CP = np.sum(vraiPositif) + np.sum(fauxNegatif)
    CN = np.sum(fauxPositif) + np.sum(vraiNegatif)
    PCP = np.sum(abs(vraiPositif)) + np.sum(fauxPositif) # predicted condition positiv
    PCN = np.sum(abs(vraiNegatif)) + np.sum(fauxNegatif) # predicted condition negative
    precision = (CP)/nbTotal
    prevalence = (CN)/ nbTotal
    PPV = np.sum(vraiPositif)/PCP # positive predicted value
    FDR = np.sum(fauxPositif) / PCP #false discovery rate
    FOR = np.sum(fauxNegatif) / PCN# false omission rate
    NPV = np.sum(vraiNegatif) / PCN # negative predictive value
    return [precision,prevalence,PPV,FDR,FOR,NPV]


def inverseMatBin(mat):
    return (abs(mat - np.ones(mat.shape))).astype(int)

def evalDesImage(srcRef,srcTest):
    """
    
    :param srcRef: 
    :param srcTest: 
    :return: 
    """
    cheminImagesRef = os.listdir(srcRef)
    cheminImagesTest = os.listdir(srcTest)
    nbImage = cheminImagesRef.__sizeof__()
    result = np.zeros([nbImage,2])
    for i in range(0,nbImage):
        imageRef = conversionBinaire(cheminImagesRef[i])
        #imgTest = cheminImagesRef   # faire tourner les algo de segmentation sur cette image
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
"""
imgTest = Image.open("D:/L3MI/2nd_Annee/Cytoo/Fibres/Stries_C2  (15)_fibre.tif")
imgTest = np.array(imgTest)
print(imgTest.shape)
imgTest = conversionBinaire(imgTest)
imaRef = Image.open("D:/L3MI/2nd_Annee/Cytoo/Fibres/Stries_C2  (16)_fibre.tif")
imaRef = np.array(imaRef)
imaRef = conversionBinaire(imaRef)
print(evalUneImage(imgTest,imaRef)) """