import numpy as np
import cv2
from PIL import Image
from Model.SegmentationGabor import SegmentationGabor

class ControlerSegmentationGabor:


    imgchemin = "D:/L3MI/2nd_Annee/Cytoo/Images_stage - Copie/Stries_C2  (44).tif"
    matImg = cv2.imread(imgchemin)
    csize = 50
    lsize = 50
    thetaMin = -0.4
    thetaMAx = 0.45
    pasTheta = 0.2
    sigma = 2
    gamma = 5
    lambdaMin = 6
    lambdaMax = 15
    pasLambda = 1
    psi = 0
    dossierSaveImgSeg = "D:/L3MI/2nd_Annee/Cytoo/testSegGabor/seg/"
    dossierSaveKernel = "D:/L3MI/2nd_Annee/Cytoo/testSegGabor/kern/"
    seg = SegmentationGabor(matImg, csize, lsize, thetaMin, thetaMAx, pasTheta, sigma, gamma, lambdaMin,lambdaMax,pasLambda, psi,dossierSaveImgSeg,dossierSaveKernel)
    img = seg.segmentation()


