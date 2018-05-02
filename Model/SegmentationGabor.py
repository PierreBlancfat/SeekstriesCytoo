import numpy as np
import cv2
from PIL import Image
import scipy
import time
import skimage.exposure as exposure


class SegmentationGabor:

    def __init__(self,matImg,csize=50, lsize=50, thetaMin=-0.4, thetaMax=0.45, pasTheta=0.2, sigma=2, gamma=5, lambdaMin=6,lambdaMax=15,pasLambda=2, psi=0,dossierSaveImgSeg = None,dossierSaveKernel=None):

        self.matImg = matImg
        self.csize = csize
        self.lsize = lsize
        self.thetaMin = thetaMin
        self.thetaMax = thetaMax
        self.pasTheta = pasTheta
        self.sigma = sigma
        self.gamma = gamma
        self.lambdaMin = lambdaMin
        self.lambdaMax = lambdaMax
        self.pasLambda = pasLambda
        self.psi = psi
        self.dossierSaveImgSeg = dossierSaveImgSeg
        self.dossierSaveKernel = dossierSaveKernel
        self.filters = None

    def build_filters(self,csize,lsize,thetaMin,thetaMax,pasTheta,sigma,gamma,lambdaMin,lambdaMax,pasLambda,psi):
        filters = []
        for lambd in np.arange(lambdaMin,lambdaMax,pasLambda):
            for theta in np.arange(thetaMin, thetaMax, pasTheta):
                kern = cv2.getGaborKernel((lsize, csize), sigma*(lambd/3), theta, lambd, gamma, psi, ktype=cv2.CV_64F)
                filters.append(kern/1.5)
                #if theta == thetaMin and self.dossierSaveKernel != None:
                #    Image.fromarray(kern).save(self.dossierSaveKernel+str(time.time())+" "+str([sigma, theta, lambd, gamma, psi]).replace(".","-")+".tif")
        self.filters = filters


    def process(self,img,filters):
        for kern in filters:
            fimg = cv2.filter2D(img, cv2.CV_8UC3, kern)
        return fimg



    def gabor(self,imgG,csize,lsize,thetaMin,thetaMax,pasTheta,sigma,gamma,lambdaMin,lambdaMax,pasLambda,psi):
        if self.filters == None:
            self.build_filters(csize,lsize,thetaMin,thetaMax,pasTheta,sigma,gamma,lambdaMin,lambdaMax,pasLambda,psi)
        res1 = self.process(imgG,self.filters)
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



    def conversionBinaire(selg,img):
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



    def paramToString(self):
        return self.thetaMin.__str__() + " " + self.thetaMax.__str__() + " " + self.pasTheta.__str__() + " " + self.sigma.__str__() + " " + self.gamma.__str__() + " " + self.lambdaMin.__str__() + " " + self.lambdaMax.__str__() + " " + self.pasLambda.__str__() + " " + self.psi.__str__()

    #Segmentation.py
    def segmentation(self):
        """
        Segmente une image avec les filtres de Gabor
        :param matImg: un emtrice représentant une image
        :return: Le masque représentant la segmentation 
        """
        #gabor segmentation
        matImg2 = self.matImg[:,:,0]
        matImg2 = exposure.equalize_adapthist(matImg2)*255
        imgSeg = self.gabor(matImg2,self.csize,self.lsize,self.thetaMin,self.thetaMax,self.pasTheta,self.sigma,self.gamma,self.lambdaMin,self.lambdaMax,self.pasLambda,self.psi)
        ret, imgSeg = cv2.threshold(imgSeg, 230, 255, cv2.THRESH_BINARY)
        # Image.fromarray(imgSeg*7000).show()
        #self.matImg[:,:,2] = imgSeg
        # if ( self.dossierSaveImgSeg != None):
        #     Image.fromarray(self.matImg).save(self.dossierSaveImgSeg+str(time.time())+".png")
        #application de flou
        imgSeg = cv2.blur(imgSeg, (27, 30), 5)
        #open
        kernel = np.ones((31, 51), np.uint8)
        imgSeg = cv2.morphologyEx(imgSeg, cv2.MORPH_OPEN, kernel)
        return self.inverseMatBin(self.conversionBinaire(imgSeg))

    def inverseMatBin(self,mat):
        return (abs(mat - np.ones(mat.shape))).astype(int)
