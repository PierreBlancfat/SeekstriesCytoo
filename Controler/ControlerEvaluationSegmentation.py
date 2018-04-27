from Model.EvaluationSegmentation import EvaluationSegmentation
from Model.SegmentationGabor import SegmentationGabor
from Model.SegmentationLBP import SegmentationLBP
import numpy as np
import time
# Amélioration possible :
    # pour chaque angle à une fréquence donné, taille fixé assez grande, faire varier la largeur
    # avec la frequence trouvé, faire varier la taille
    # idée : adapté le filtre en elipsoïde
    # -> coupler les méthodes de gabor et LBP aux méthodes statistique
    # -> faire des coupes réctangulaires
def evaluationParametreGabor(self):
    """
    Evalue la segmentation par gabor pour une plage de données 
    :return: stat : une liste contenant les paramètres utilisé et le resultat
    """
    # Choix de la plage de paramètre à tester pour gabor
    # Pour boucle de création de kernel*
    #taille du kernel en pixel
    csize = 50
    lsize = 50

    # angle en radian
    thetaMin = -0.4
    thetaMax = 0.45
    pasTheta = 0.2
    # longueur d'onde en pixel
    lambdaMin = 4
    lambdaMax = 15
    pasLambda = 2

    # pour variation des paramètres
    # ecart type gaussienne
    sigmaMin = 2
    sigmaMax = 3
    pasSigma = 2

    # spacial aspect ration
    gamaMin = 5
    GamaMax = 6
    pasGama = 1

    # décalage
    psiMin = 0
    psiMax = 1
    pasPsi = 2


    dossierSaveImgSeg = "D:/L3MI/2nd_Annee/Cytoo/testSegGabor/seg/"
    dossierSaveKernel = "D:/L3MI/2nd_Annee/Cytoo/testSegGabor/kern/"

    srcDossierImageRef = "D:/L3MI/2nd_Annee/Cytoo/Stries"
    srcDossiertest = "D:/L3MI/2nd_Annee/Cytoo/StriesTest"

    """
    Evalue une plage de paramètres données à la fonction de segmentation de Gabor
    :return: Une liste donnant les paramètres données et le résulat de l'évaluation 
    """
    stat = list()
    timer = time.time()
    for sigma in np.arange(sigmaMin,sigmaMax, pasSigma):
        for psi in np.arange(psiMin,psiMax,pasPsi):
            for gamma in np.arange(gamaMin,GamaMax,pasGama):
                segGabor = SegmentationGabor(None,csize, lsize, thetaMin, thetaMax, pasTheta, sigma, gamma, lambdaMin,lambdaMax,pasLambda, psi,dossierSaveImgSeg,dossierSaveKernel)
                print(segGabor.paramToString())
                evaluateur = EvaluationSegmentation(srcDossierImageRef,srcDossiertest,segGabor)
                reslt = evaluateur.evalDesImages(segGabor)
                listReturn = [csize, lsize, thetaMin, thetaMax, pasTheta, sigma, gamma, lambdaMin,lambdaMax,pasLambda, psi,reslt.tolist()]
                print(reslt)
                stat.append(listReturn)
    print(time.time() - timer)
    return stat



#main
stat = evaluationParametreGabor(None)
