import cv2
import math
import os
import numpy as np
from PIL import Image
import scipy
import Modele.SegmentationGabor
def evalUneImage(imgRef,imgTest):
    """
    Evaluation de la qualité d'une segmentation 
    :param imgRef: une matrice binaire
    :param imgTest: une matrice binaire
    :return: [precision,prevalence,PPV,FDR,FOR,NPV]
    """
    print(len(imgRef.shape))
    if len(imgRef.shape)== 3: # si l'image à plusieurs composantes
      imgRef = imgRef[:,:,1]
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
    FDR = np.sum(fauxPositif) / PCP # false discovery rate
    FOR = np.sum(fauxNegatif) / PCN # false omission rate
    NPV = np.sum(vraiNegatif) / PCN # negative predictive value
    return [precision,prevalence,PPV,FDR,FOR,NPV]


def inverseMatBin(mat):
    return (abs(mat - np.ones(mat.shape))).astype(int)

def evalDesImages(srcRef,srcTest,algoSegmentation):
    """
    :param srcRef: chemin du dossier reference ( masque binaire)
    :param srcTest:v chemin du dossier des images test
    :return: une matrice avec autant de lignes que d'images
    """
    nomsImagesRef = os.listdir(srcRef)
    nomsImagesTest = os.listdir(srcTest)
    indice = 0
    result = np.zeros((150,6))
    print(nomsImagesRef)
    for imgTest in nomsImagesTest: # pour chaque image à tester
        imgTest = imgTest[:-4]
        if any(imgTest in s for s in nomsImagesRef): #si le masque existe
            print(imgTest)

            indexMasque = nomsImagesRef.index(imgTest+"_s.tif") #recupérer l'index du masque dand la liste
            cheminImageTest = srcTest+"/"+imgTest+".tif"        # construit le chemin de l'image à tester
            cheminImageRef = srcRef+"/"+nomsImagesRef[indexMasque] #construit le chemin du masque
            imgTest = cv2.imread(cheminImageTest)     #lecture de l'image
            imgRef = np.array(Image.open(cheminImageRef))
            imgTestSeg = inverseMatBin(algoSegmentation(imgTest))
            imgRef = conversionBinaire(imgRef)
           # Image.fromarray((imgTestSeg)).show()
           #Image.fromarray(imgRef*100+imgTestSeg*100).show()
            result[indice]  = evalUneImage(imgRef,imgTestSeg)
            indice+=1
    print(indice)
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
     imarray = imarray.astype(int) # converti en int
     return  imarray


#main  test
# imgTest = Image.open("D:/L3MI/2nd_Annee/Cytoo/Fibres/Stries_C2  (26)_fibre.tif")
# imgTest = np.array(imgTest)
# imgTest = conversionBinaire(imgTest)
# imaRef = Image.open("D:/L3MI/2nd_Annee/Cytoo/Fibres/Stries_C2  (25)_fibre.tif")
# imaRef = np.array(imaRef)
# imaRef = conversionBinaire(imaRef)
# print(evalUneImage(imgTest,imaRef))

tabREsult = evalDesImages("D:/L3MI/2nd_Annee/Cytoo/Stries","D:/L3MI/2nd_Annee/Cytoo/Images_stage_stries",Modele.SegmentationGabor.segmentaionGabor)
tabREsultSum = np.sum(tabREsult,axis=0)/137
print(tabREsultSum)