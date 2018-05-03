import numpy as np
import cv2
from PIL import Image
import scipy
import time
import skimage.exposure as exposure
from Model.preTraitementImg import HPF


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

    def gabor(self, imgG, csize, lsize, thetaMin, thetaMax, pasTheta, sigma, gamma, lambdaMin, lambdaMax, pasLambda,
              psi):
        """
        Main fonction, call buildfilter anc process
        :return: 
        """
        if self.filters == None:
            self.build_filters(csize, lsize, thetaMin, thetaMax, pasTheta, sigma, gamma, lambdaMin, lambdaMax,pasLambda, psi)
        res1 = self.process(imgG, self.filters)
        return res1

    def build_filters(self,csize,lsize,thetaMin,thetaMax,pasTheta,sigma,gamma,lambdaMin,lambdaMax,pasLambda,psi):
        """
        Builds gabor filter
        :return: A list with the gabor filter
        """
        filters = []
        for lambd in np.arange(lambdaMin,lambdaMax,pasLambda):
            for theta in np.arange(thetaMin, thetaMax, pasTheta):
                kern = cv2.getGaborKernel((lsize, csize), sigma*(lambd/3), theta, lambd, gamma, psi, ktype=cv2.CV_64F)
                filters.append(kern/1.5)
        self.filters = filters


    def process(self,img,filters):
        """
        Convolution of each gabor filter
        :param img: a matrix which represents a picture
        :param filters: a list of matrix which represents gabor filters
        :return: The response of the convolution 
        """
        for kern in filters:
            fimg = cv2.filter2D(img, cv2.CV_8UC3, kern)
        return fimg


    def segmentation(self):
        """
        Segmentation of a image
        :param matImg: a matrix which reresents an image
        :return: a mask which represent the segmentation. 1 means the algorithm detect a striation, 
        """
        #pre-traitement
        matImg2 = self.matImg[:,:,0]
        matImg2 = exposure.equalize_adapthist(matImg2)*255 # egalisation local du contraste
        # matImg2 = HPF(matImg2,2)
        #gabor
        imgSeg = self.gabor(matImg2,self.csize,self.lsize,self.thetaMin,self.thetaMax,self.pasTheta,self.sigma,self.gamma,self.lambdaMin,self.lambdaMax,self.pasLambda,self.psi)
        ret, imgSeg = cv2.threshold(imgSeg, 254, 255, cv2.THRESH_BINARY)
        # Image.fromarray(imgSeg*7000).show()
        #self.matImg[:,:,2] = imgSeg
        if ( self.dossierSaveImgSeg != None):
            Image.fromarray(self.matImg).save(self.dossierSaveImgSeg+str(time.time())+".png")
        #application de flou
        imgSeg = cv2.blur(imgSeg, (27, 30), 5)
        #open
        kernel = np.ones((31, 51), np.uint8)
        imgSeg = cv2.morphologyEx(imgSeg, cv2.MORPH_OPEN, kernel)
        return self.inverseMatBin(self.conversionBinaire(imgSeg))


    def conversionBinaire(self,img):
         """
        Convert a matrix into a binary matrix
         :param img: a int matrix 
         :return: a binary matrix
         """
         imarray = np.array(img) # image to np array
         imarray = scipy.sign(imarray)  # binarize
         imarray = np.floor(abs(imarray - np.ones(imarray.shape))) #inversion 1 -> 0, 0-> 1
         imarray = imarray.astype(int) # convertie en int
         return  imarray


    def paramToString(self):
        return self.thetaMin.__str__() + " " + self.thetaMax.__str__() + " " + self.pasTheta.__str__() + " " + self.sigma.__str__() + " " + self.gamma.__str__() + " " + self.lambdaMin.__str__() + " " + self.lambdaMax.__str__() + " " + self.pasLambda.__str__() + " " + self.psi.__str__()

    #Segmentation.py


    def inverseMatBin(self,mat):
        """
        Create the inverse of a binary matrix, 0 become 1, 1 become 0
        :param mat: a binary matrix
        :return: a binary matrix
        """
        return (abs(mat - np.ones(mat.shape))).astype(int)

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
