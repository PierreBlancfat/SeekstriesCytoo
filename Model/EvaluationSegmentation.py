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

    def evalUneImage(self,maskRef,maskTest):
        """
        Evalutation of a segmentation on one picture
        :param maskRef: A binary matrix which represents the segmentation by hand
        :param maskTest: A binary matrix which represents the segmentation by the computer
        :return:[precision,prevalence,PPV,FDR,FOR,NPV,TPR,FPR,FNR,TNR,LRplus,LRmoins,vraivrai] : Some statistics about the quality of the segmentation
        """
        if len(maskRef.shape) == 3: # si l'image à plusieurs composantes
            maskRef = maskRef[:,:,0]
        if len(maskTest.shape) == 3: # si l'image à plusieurs composantes
            maskTest = maskTest[:,:,0]
        nbTotal = maskRef.size
        vraiPositifMat = (maskRef & maskTest)
        inverseRefMat = self.inverseMatBin(maskRef)
        fauxPositifMat = inverseRefMat & maskTest
        fauxNegatifMat = maskTest & self.inverseMatBin(vraiPositifMat)
        vraiNegatifMat= self.inverseMatBin(maskTest | maskRef)
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
        """
        Create the inverse of a binary matrix, 0 become 1, 1 become 0
        :param mat: a binary matrix
        :return: a binary matrix
        """
        return (abs(mat - np.ones(mat.shape))).astype(int)

    def evalDesImages(self,algoSegmentation):
        """
        Evalutate the segmentation of many pictures
        :param algoSegmentation: the algorithm used for the segmentation 
        :return: the mean of [precision,prevalence,PPV,FDR,FOR,NPV,TPR,FPR,FNR,TNR,LRplus,LRmoins,vraivrai] 
        """
        nomsImagesRef = os.listdir(self.srcDossierImageRef)
        nomsImagesTest = os.listdir(self.srcDossiertest)
        indice = 0
        result = np.zeros((150,13))
        for nomImgTest in nomsImagesTest: # pour chaque image à tester
            nomImgTest = nomImgTest[:-4]
            if any(nomImgTest in s for s in nomsImagesRef): #si le masque existe
                try:
                    indexMasqueS = nomsImagesRef.index(nomImgTest+"_s.TIF")     #recup# érer l'index du masque dand la liste
                    indexMasqueP = nomsImagesRef.index(nomImgTest +"_p.TIF")  # recupérer l'index du masque dand la listeindex du masque dand la liste
                except:
                    indexMasqueS = nomsImagesRef.index(nomImgTest + "_s.tif")  # recup# érer l'index du masque dand la liste
                    indexMasqueP = nomsImagesRef.index(nomImgTest + "_p.tif")  # recupérer l'index du masque dand la listeindex du masque dand la liste
                cheminImageTest = self.srcDossiertest+"/"+nomImgTest+".TIF"        # construit le chemin de l'image à tester
                cheminImageRef1 = self.srcDossierImageRef+"/"+nomsImagesRef[indexMasqueS] #construit le chemin du masque1
                cheminImageRef2 = self.srcDossierImageRef+"/"+nomsImagesRef[indexMasqueP] #construit le chemin du masque2
                imgTest = cv2.imread(cheminImageTest)   #lecture de l'image
                algoSegmentation.matImg = imgTest
                maskTestSegGab = algoSegmentation.segmentation()
                print(maskTestSegGab.shape)
                imgTest[:,:,2] = maskTestSegGab*100
                Image.fromarray(imgTest).save("../Data/testSegGabor/seg/"+str(time.time())+"_"+nomImgTest+".tif")
                imgRef = self.conversionBinaire(np.array(Image.open(cheminImageRef1)))
                segFibre = SegmentationFibre(imgTest)
                maskFibre = segFibre.segmenter()
                result[indice] = self.evalUneImage(imgRef,maskTestSegGab.astype(int)&maskFibre.astype(int))
                indice+=1
        print(np.sum(result,axis=0)/indice)
        return np.sum(result,axis=0)/indice

    def conversionBinaire(self,img):
         """
         Convert a matrix into a binary matrix
         :param img: a matrix 
         :return: a binary matrix
         """
         imarray = np.array(img) # image to np array
         imarray = scipy.sign(imarray)  # binarize
         imarray = np.floor(abs(imarray - np.ones(imarray.shape))) #inversion 1 -> 0, 0-> 1
         imarray = imarray.astype(int) # convertie en int
         return  imarray


