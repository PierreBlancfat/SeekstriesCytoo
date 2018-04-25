

########################################################################################
#                                                                                      #
# Script pour faire un pré-traitement sur les images avant d'appliquer nos algorithmes #
#                                                                                      #
########################################################################################

import matplotlib.pyplot as plt
import numpy as np
import cv2


img = cv2.imread('test.TIF',0) # Image de test


def LPF(img,n):
    '''
    Low-pass filters aide à réduire le bruit dans une image
    @param img: image à traiter (créer précédemment grâce à "imread()")
    @param n:  numéro du filtre appliqué (1 = soft, 2 = rough)
    @return: -1 si il y a eu une erreur, sinon l'image après filtrage
    '''
    if (n==1):
        LPF1 = np.ones((3,3),np.float32)/9
        return cv2.filter2D(img,-1,LPF1)
    elif (n==2):
        LPF2 = np.ones((5,5),np.float32)/50
        return cv2.filter2D(img,-1,LPF2)
    else:
        print('Appel LPF : Numéro filtre incorrect')
        return -1


def HPF(img,n):
    '''
    High-pass filters aide à trouver les edges dans une image
    @param img: image à traiter (créer précédemment grâce à "imread()")
    @param n:  Pourcentage (0 < n < 100) du filtre
    @return: -1 si il y a eu une erreur, sinon l'image après filtrage
    '''
    if (n>=0 and n<=100):
        HPF1 = -1 * np.ones((5, 5))
        HPF1[3][3] = 25*(n/100)
        return cv2.filter2D(img,-1,HPF1)
    else:
        print('Appel HPF : Numéro filtre incorrect')
        return -1


def GB(img,n):
    '''
    Gaussian Blur (floute l'image)
    @param img: image à traiter (créer précédemment grâce à "imread()")
    @param n:  numéro du filtre appliqué (1 = basique)
    @return: -1 si il y a eu une erreur, sinon l'image après filtrage
    '''
    if (n==1):
        return cv2.GaussianBlur(img,(5,5),0)
    else:
        print('Appel Gaussian Blur : Numéro filtre incorrect')
        return -1


def BLF(img,n):
    '''
    Bilateral filters is highly effective in noise removal while keeping edges sharp
    @param img: image à traiter (créer précédemment grâce à "imread()")
    @param n:  numéro du filtre appliqué (1 = basique)
    @return: -1 si il y a eu une erreur, sinon l'image après filtrage
    '''
    if (n==1):
        return cv2.bilateralFilter(img,5,75,75)
    else:
        print('Appel BLF : Numéro filtre incorrect')
        return -1

def contrastAndBrightness(img,alpha,beta):
    '''
    Augmente / Diminue le contrast et le brightness de l'image
    @param img: image à traiter (créer précédemment grâce à "imread()")
    @param alpha: appartient à [1.0 ; 3.0] représente l'augementation du contraste
    @param beta: appartient à [0 ; 100] représente l'augmentation du brightness
    @return: -1 si erreur, l'image traité sinon
    '''

    if (alpha>=0.0 and alpha<=3.0 and beta>=0 and beta<=100):
        for i in range(len(img)):
            for j in range(len(img[0])):
                img[i][j] = int(alpha * img[i][j] + beta)

    return img