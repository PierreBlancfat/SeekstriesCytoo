#!/usr/bin/env python

import numpy as np
import cv2
from matplotlib import pyplot as plt
from PIL import Image
import scipy
import random


thetaBase = 0
amplitude = 1

def build_filters(theta,sigma):
    filters = []
    ksize = 36
    amp = 1.5
    pas = 0.2
    for sigma in np.arange(sigma-amp,sigma+amp,pas):
         kern = cv2.getGaborKernel((ksize, ksize), sigma, theta, 7.8, 1, 0, ktype=cv2.CV_32F)
         kern /= 1.5 * kern.sum()
    cv2.imshow("kern",kern)
    filters.append(kern)
    return filters


def process(img, filters):
    accum = np.zeros_like(img)
    for kern in filters:
        fimg = cv2.filter2D(img, cv2.CV_8UC3, kern)
    np.maximum(accum, fimg, accum)
    return accum



def gabor(theta,sigma,imgG):
    filters = build_filters(theta,sigma)

    res1 = process(imgG, filters)
    plt.subplot(3,1,2)
    #plt.imshow(res1, cmap='gray', interpolation='bicubic')

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
def segmentaionGabor(matImg):
    """
    Segmente une image avec les filtres de Gabor
    :param matImg: un emtrice représentant une image
    :return: Le masque représentant la segmentation 
    """
    #gabor segmentation
    matImg2 = matImg[:,:,1]
    theta = 3.3
    sigma = 3.6
    imgSeg = gabor(theta, sigma,matImg2)
    ret, imgSeg = cv2.threshold(imgSeg, 254, 255, cv2.THRESH_BINARY)
    matImg[:,:,2] = imgSeg
    Image.fromarray(matImg).save("D:/L3MI/2nd_Annee/Cytoo/testSegGabor/"+str(random.randint(1,999999))+".png")
    #application de flou
    imgSeg = cv2.blur(imgSeg, (20, 20), 5)
    imgSeg = cv2.blur(imgSeg, (20, 20), 5)
    return conversionBinaire(imgSeg)








    # # active contour model
# img = Image.fromarray(imgSeg)
# img = data.astronaut()
# img = rgb2gray(img)
# s = np.linspace(0, 2*np.pi, 400)
# x = 220 + 100*np.cos(s)
# y = 100 + 100*np.sin(s)
# init = np.array([x, y]).T
#
# img = imgSeg
# snake = active_contour(gaussian(img, 3), init, alpha=0.015, beta=10, gamma=0.001)
#
# fig, ax = plt.subplots(figsize=(7, 7))
# ax.imshow(img, cmap=plt.cm.gray)
# ax.plot(init[:, 0], init[:, 1], '--r', lw=3)
# ax.plot(snake[:, 0], snake[:, 1], '-b', lw=3)
# ax.set_xticks([]), ax.set_yticks([])
# ax.axis([0, img.shape[1], img.shape[0], 0])
# Image.fromarray(imgSeg).show()
# imgSeg = kMeans(imgSeg,4)