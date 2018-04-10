import cv2
import math
import os



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
    return (pourcentagePositif,pourcentageNegatif)


def evalDesImage(srcRef,srcTest):
    cheminImagesRef = os.listdir(srcRef)
    cheminImagesTest = os.listdir(srcTest)

    for i in range(0,cheminImagesRef.__sizeof__()):
        result = evalUneImage



#main  test
