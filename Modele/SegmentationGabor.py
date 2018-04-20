#!/usr/bin/env python

import numpy as np
import cv2
from matplotlib import pyplot as plt
from PIL import Image
import scipy
import time


def build_filters(csize,lsize,thetaMin,ThetaMax,pasTheta,sigma,gamma,lambdaMin,lambdaMax,pasLambda,psi):
    filters = []
    for theta in np.arange(thetaMin,ThetaMax,pasTheta):
        for lambd in np.arange(lambdaMin,lambdaMax,pasLambda):
             kern = cv2.getGaborKernel((lsize, csize), sigma, theta, lambd, gamma, psi, ktype=cv2.CV_32F)
             if theta == thetaMin:
                 # Image.fromarray(kern*255).show()
                 Image.fromarray(kern).save("D:/L3MI/2nd_Annee/Cytoo/testSegGabor/kern/"+str([sigma, theta, lambd, gamma, psi]).replace(".","-")+".tif")
             filters.append(kern)
    return filters


def process(img, filters):
    accum = np.zeros_like(img)
    for kern in filters:
        fimg = cv2.filter2D(img, cv2.CV_8UC3, kern)
    np.maximum(accum, fimg, accum)
    return accum



def gabor(imgG,csize,lsize,thetaMin,ThetaMax,pasTheta,sigma,gamma,lambdaMin,lambdaMax,pasLambda,psi):
    filters = build_filters(csize,lsize,thetaMin,ThetaMax,pasTheta,sigma,gamma,lambdaMin,lambdaMax,pasLambda,psi)
    res1 = process(imgG, filters)
    return res1


def kMeans(img,k):
    '''
    Applique la méthode des k-means sur une image pour la segmenter
    @param img: image à traiter (créer précédemment grâce à "imread()")
    @param k: nombre de clusters
    @return: l'image après traitement
    '''

    # convert to np.float32
    res = img.reshape((-1, 3))
    res = np.float32(res)

    # define criteria, number of clusters(K) and apply kmeans()
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    ret, label, center = cv2.kmeans(res, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

    # Now convert back into uint8, and make original image
    center = np.uint8(center)
    res = center[label.flatten()]
    res = (res/np.min(res))-1 # normaliser à 0
    res = scipy.sign(res) # Binarisation
    res = res * 255 # pour afficher en noir blanc
    res2 = res.reshape((img.shape))
    return res2



def conversionBinaire(img):
     """
     Convertie une image en binaire
     :param srcImageRef: Le chemin de l'image 
     :return: Une matrice binaire de même taille que l'image source. Les 1 représentent le "noir" ( zone positive), le 0 le "blanc" ( zone négative)
     """
     imarray = np.array(img) # image to nparray
     imarray = scipy.sign(imarray)  # binarise
     imarray = np.floor(abs(imarray - np.ones(imarray.shape))) #inversion 1 -> 0, 0-> 1
     imarray = imarray.astype(int) # converti en int
     return  imarray


imgchemin = "D:/L3MI/2nd_Annee/Cytoo/Images_stage - Copie/Stries_C2  (44).tif"



#Segmentation
def segmentationGabor(matImg,csize,lsize,thetaMin,thetaMAx,pasTheta,sigma,gamma,lambdaMin,lambdaMax,pasLambda,psi):
    """
    Segmente une image avec les filtres de Gabor
    :param matImg: un emtrice représentant une image
    :return: Le masque représentant la segmentation 
    """
    #gabor segmentation
    matImg2 = matImg[:,:,0]
    matImg2 = cv2.blur(matImg2,(3,3))
    imgSeg = gabor(matImg2,csize,lsize,thetaMin,thetaMAx,pasTheta,sigma,gamma,lambdaMin,lambdaMax,pasLambda,psi)
    ret, imgSeg = cv2.threshold(imgSeg, 254, 255, cv2.THRESH_BINARY)
    matImg[:,:,2] = imgSeg
    Image.fromarray(matImg).save("D:/L3MI/2nd_Annee/Cytoo/testSegGabor/"+str(time.time())+".png")
    # Image.fromarray(matImg).show()
    #application de flou
    imgSeg = cv2.blur(imgSeg, (20, 20), 5)
    return conversionBinaire(imgSeg)



#main
matImg = cv2.imread(imgchemin)
csize = 40
lsize = 40
thetaMin = -0.8
thetaMAx = 0.8
pasTheta = 0.8
sigma = 6.2
gamma = 1.5 
lambdaMin = 4
lambdaMax = 12
pasLambda = 0.5
psi = 0

img = segmentationGabor(matImg, csize, lsize, thetaMin, thetaMAx, pasTheta, sigma, gamma, lambdaMin,lambdaMax,pasLambda, psi)
