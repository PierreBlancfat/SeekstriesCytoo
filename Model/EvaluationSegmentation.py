import cv2
import os
import numpy as np
from PIL import Image
import scipy
from Model.SegmentationFibre import SegmentationFibre
import time


class EvaluationSegmentation:


    def __init__(self,srcDossierImageRef,srcDossiertest,algoSegmentation):    #Choix de la plage de paramètre à tester pour gabor
        #Pour boucle de création de kernel*
        #angle

        self.algoSegmentation = algoSegmentation
        self.srcDossierImageRef = srcDossierImageRef
        self.srcDossiertest = srcDossiertest

    def evalUneImage(self,imgRef,imgTest):
        """
        Evaluation de la qualité d'une segmentation
        :param imgRef: une matrice binaire
        :param nomImgTest: une matrice binaire
        :return: [precision,prevalence,PPV,FDR,FOR,NPV,TPR,FPR,FNR,TNR,LRplus,LRmoins,vraivrai]
        """
        if len(imgRef.shape) == 3: # si l'image à plusieurs composantes
          imgRef = imgRef[:,:,0]
        if len(imgTest.shape) == 3: # si l'image à plusieurs composantes
            imgTest = imgTest[:,:,0]
        nbTotal = imgRef.size
        vraiPositifMat = (imgRef & imgTest)
        inverseRefMat = self.inverseMatBin(imgRef)
        fauxPositifMat = inverseRefMat & imgTest
        vraiNegatifMat = imgRef & self.inverseMatBin(vraiPositifMat)
        fauxNegatifMat= self.inverseMatBin(imgTest | imgRef)
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


    def inverseMatBin(self, mat):
        return (abs(mat - np.ones(mat.shape))).astype(int)

    def evalDesImages(self,algoSegmentation):
        """
        :param srcRef: chemin du dossier reference ( masque binaire)
        :param srcTest:v chemin du dossier des images test
        :return: une matrice avec autant de lignes que d'images
        """
        nomsImagesRef = os.listdir(self.srcDossierImageRef)
        nomsImagesTest = os.listdir(self.srcDossiertest)
        indice = 0
        result = np.zeros((150,13))
        for nomImgTest in nomsImagesTest: # pour chaque image à tester
            nomImgTest = nomImgTest[:-4]
            if any(nomImgTest in s for s in nomsImagesRef): #si le masque existe
                indexMasqueS = nomsImagesRef.index(nomImgTest+"_s.TIF")   #recupérer l'index du masque dand la liste
                indexMasqueP = nomsImagesRef.index(nomImgTest + "_p.TIF")  # recupérer l'index du masque dand la liste
                cheminImageTest = self.srcDossiertest+"/"+nomImgTest+".TIF"        # construit le chemin de l'image à tester
                cheminImageRef1 = self.srcDossierImageRef+"/"+nomsImagesRef[indexMasqueS] #construit le chemin du masque1
                cheminImageRef2 = self.srcDossierImageRef+"/"+nomsImagesRef[indexMasqueP] #construit le chemin du masque2
                imgTest = cv2.imread(cheminImageTest)   #lecture de l'image
                #Segmentation
                algoSegmentation.matImg = imgTest      #donne la matrice à l'algo Segmentation.py
                maskTestSegGab = algoSegmentation.segmentation()
                imgTest[:,:,2] = maskTestSegGab*100
                Image.fromarray(imgTest).save("../Data/testSegGabor/seg/"+str(time.time())+"_"+nomImgTest+".tif")
                imgRef = self.conversionBinaire(np.array(Image.open(cheminImageRef1))) |  self.conversionBinaire(np.array(Image.open(cheminImageRef2)))
                segFibre = SegmentationFibre(imgTest)
                maskFibre = segFibre.segmenter()
                result[indice] = self.evalUneImage(imgRef,maskTestSegGab&maskFibre.astype(int))

                indice+=1
        return np.sum(result,axis=0)/indice

    def conversionBinaire(self,img):
         """
         Convertie une image en binaire
         :param srcImageRef: Le chemin de l'image
         :return: Une matrice binaire de même taille que l'image source. Les 1 représentent le "noir" ( zone positive), le 0 le "blanc" ( zone négative)
         """
         imarray = np.array(img) # image to np array
         imarray = scipy.sign(imarray)  # binarize
         imarray = np.floor(abs(imarray - np.ones(imarray.shape))) #inversion 1 -> 0, 0-> 1
         imarray = imarray.astype(int) # convertie en int
         return  imarray



    def concatMasque(self,masque1,masque2):
        """
        Concatène des masques binaires
        :param masque1: une matrice binaire
        :param masque2: une matrice binaire
        :return: (masque1 & masque2)
        """
        return masque1 & masque2

    def propStries(self, masqueFibre, masqueStries):
        """
        Calcul la proportion de stries dans une fibre
        :param masqueFibre: une matrice binaire
        :param masqueStries: une matrice binaire
        :return: proportion des stries dans la fibre
        """
        perimFibre = np.sum(masqueFibre)
        masqueStries = np.logical_and(masqueFibre,masqueStries)
        perimStriesFi=np.sum(masqueStries)
        return perimStriesFi/perimFibre
