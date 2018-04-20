import cv2
import math
import os
import numpy as np
from PIL import Image
import scipy
import Modele.SegmentationGabor
from tempfile import TemporaryFile


def evalUneImage(imgRef,imgTest):
    """
    Evaluation de la qualité d'une segmentation 
    :param imgRef: une matrice binaire
    :param imgTest: une matrice binaire
    :return: [precision,prevalence,PPV,FDR,FOR,NPV]
    """
    if len(imgRef.shape)== 3: # si l'image à plusieurs composantes
      imgRef = imgRef[:,:,0]
    nbTotal = imgRef.size
    vraiPositifMat = (imgRef & imgTest)
    inverseRefMat = inverseMatBin(imgRef)
    fauxPositifMat = inverseRefMat & imgTest
    vraiNegatifMat = imgRef & inverseMatBin(vraiPositifMat)
    fauxNegatifMat= inverseMatBin(imgTest | imgRef)
    vraiPositif = np.sum(vraiPositifMat)
    fauxPositif =np.sum(fauxPositifMat)
    vraiNegatif =  np.sum(vraiNegatifMat)
    fauxNegatif = np.sum(fauxNegatifMat)
    CP = vraiPositif + fauxNegatif
    CN = fauxPositif + vraiNegatif
    PCP = vraiPositif + fauxPositif + 1# predicted condition positiv
    PCN = vraiNegatif + fauxNegatif + 1 # predicted condition negative
    precision = (CP)/nbTotal
    prevalence = (CN)/ nbTotal
    PPV = vraiPositif / PCP # positive predicted value
    FDR = fauxPositif / PCP # false discovery rate
    FOR = fauxNegatif / PCN # false omission rate
    NPV = vraiNegatif / PCN # negative predictive value
    VPV =  vraiNegatif + vraiPositif+1
    #
    FNR = 0
    TPR = 0
    if(CP != 0):
        FNR = fauxNegatif / CP # false negative RAte
        TPR = vraiPositif / CP  #True positive rate
    #
    FPR = 0
    TNR = 0
    if(CN != 0):
        FPR = fauxPositif /  CN #False positive Rate
        TNR = vraiNegatif / CN  #True negative rate

    LRplus =  0
    LRmoins = 0
    if FDR != 0:
         LRplus = TPR/FPR
    if TNR != 0:
        LRmoins = FNR/TNR
    # print([precision,prevalence,PPV,FDR,FOR,NPV,TPR,FPR,FNR,TNR,LRplus,LRmoins])
    vraivrai = vraiPositif/VPV
    return [precision,prevalence,PPV,FDR,FOR,NPV,TPR,FPR,FNR,TNR,LRplus,LRmoins,vraivrai]


def inverseMatBin(mat):
    return (abs(mat - np.ones(mat.shape))).astype(int)

def evalDesImages(srcRef,srcTest,algoSegmentation,csize,lsize,thetaMin,thetaMax,pasTheta,sigma,gamma,lambdaMin,lambdaMax,pasLambda,psi):
    """
    :param srcRef: chemin du dossier reference ( masque binaire)
    :param srcTest:v chemin du dossier des images test
    :return: une matrice avec autant de lignes que d'images
    """
    nomsImagesRef = os.listdir(srcRef)
    nomsImagesTest = os.listdir(srcTest)
    indice = 0
    result = np.zeros((150,13))
    for imgTest in nomsImagesTest: # pour chaque image à tester
        imgTest = imgTest[:-4]
        if any(imgTest in s for s in nomsImagesRef): #si le masque existe
            indexMasque = nomsImagesRef.index(imgTest+"_s.tif") #recupérer l'index du masque dand la liste
            cheminImageTest = srcTest+"/"+imgTest+".tif"        # construit le chemin de l'image à tester
            cheminImageRef = srcRef+"/"+nomsImagesRef[indexMasque] #construit le chemin du masque
            imgTest = cv2.imread(cheminImageTest)     #lecture de l'image
            imgRef = np.array(Image.open(cheminImageRef))
            imgTestSeg = inverseMatBin(algoSegmentation(imgTest,csize,lsize,thetaMin,thetaMax,pasTheta,sigma,gamma,lambdaMin,lambdaMax,pasLambda,psi))
            imgRef = conversionBinaire(imgRef)
            # if len(imgRef.shape) == 3:  # si l'image à plusieurs composantes
            #     imgRefS = imgRef[:, :, 0]
            #     # Image.fromarray(imgRefS*100+imgTestSeg*200).show()
            #     # print("hic")
            # else:
                # Image.fromarray(imgRef * 100 + imgTestSeg * 200).show()
            #Image.fromarray((imgTestSeg)).show()
            result[indice] = evalUneImage(imgRef,imgTestSeg)
            indice+=1
    return np.sum(result,axis=0)/indice

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




def evaluationParametreGabor(srcDossierImageRef,srcDossiertest,thetaMin,thetaMax,pasTheta,sigmaMin,sigmaMax,pasSigma,gamaMin,GamaMax,pasGama,lambdaMin,lambdaMax,pasLambda,psiMin,psiMax,pasPsi):
    """
    Evalue une plage de paramètres données à la fonction de segmentation de Gabor
    :return: Une liste donnant les paramètres données et le résulat de l'évaluation 
    """
    stat= list()
    csize = 54
    lsize = 54
    for sigma in np.arange(sigmaMin,sigmaMax, pasSigma):
            for psi in np.arange(psiMin,psiMax,pasPsi):
                for gamma in np.arange(gamaMin,GamaMax,pasGama):
                    print(thetaMin.__str__()+" "+thetaMAx.__str__()+" "+pasTheta.__str__()+" "+sigma.__str__()+" "+gamma.__str__()+" "+lambdaMin.__str__()+" "+lambdaMax.__str__()+" "+pasLambda.__str__()+" "+psi.__str__())
                    reslt = evalDesImages(srcDossierImageRef,srcDossiertest,Modele.SegmentationGabor.segmentationGabor,csize,lsize,thetaMin,thetaMax,pasTheta,sigma,gamma,lambdaMin,lambdaMax,pasLambda,psi)
                    listReturn = [thetaMin,thetaMax,pasTheta,sigma,gamma,lambdaMin,lambdaMax,pasLambda,psi,reslt.tolist()]
                    print(reslt)
                    stat.append(listReturn)
    return stat


#main
#Choix de la plage de paramètre à tester pour gabor

#Pour boucle de création de kernel*
#angle
thetaMin = -0.9
thetaMAx = 0.9
pasTheta = 0.3
#frequence
lambdaMin = 5
lambdaMax = 12
pasLambda = 0.5

# pour variation des paramètres
#ecart type gaussienne
sigmaMin = 6.2
sigmaMax = 7
pasSigma = 2

#spacial aspect ration
gamaMin = 1.5
GamaMax = 2
pasGama = 2

#décalage
psiMin = 0
psiMax = 1
pasPsi = 2

srcDossierImageRef= "D:/L3MI/2nd_Annee/Cytoo/Stries"
srcDossiertest=  "D:/L3MI/2nd_Annee/Cytoo/StriesTestPetit"

resultEval = evaluationParametreGabor(srcDossierImageRef,srcDossiertest,thetaMin,thetaMAx,pasTheta,sigmaMin,sigmaMax,pasSigma,gamaMin,GamaMax,pasGama,lambdaMin,lambdaMax,pasLambda,psiMin,psiMax,pasPsi)
print(resultEval)
