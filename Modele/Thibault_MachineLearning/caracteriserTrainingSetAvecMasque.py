'''
Algorithme qui :
    - propose d'afficher quels sont les rectangles striés dans le dossier
    trainingImages. 
    - associe à chaque rectangle sa caractérisation
    - place dans un fichier : la caractérisation et un booleen (strié/non strié)
'''


import numpy as np
from skimage import io
from skimage.feature import local_binary_pattern
from skimage.transform import resize
import os
'''
Pour chaque image, on affiche le quadrillage et on propose à l'utilisateur de
cliquer sur les rectangles striés.
On ajoute alors cette donnée dans le fichier, associé a sa caractérisation.
''' 

METHOD = 'uniform'

# settings for LBP
radius = 1
n_points = 8 * radius


scall = 1/2
# dimensions d'une image :
hImg = 1024*scall
lImg = 1344*scall
# nombre de rectangles :
nbRecH = int(32*scall)
nbRecL = int(24*scall)
# dimensions d'un rectangle :
hRec = int(hImg/nbRecH)
lRec = int(lImg/nbRecL)
# taille d'un vecteur caractérisant un sous rectangle
vecSize = 28



'''
===============================================
====== FONCTIONS DE GESTION DE FICHIER : ======
===============================================
'''
import csv
def initWriter(filePath) :
    """
    Ouvre un fichier a partir de son chemin "filePath" et cree
    un objet transcripteur pour ecrire dans ce fichier.
    - filePath : le chemin du fichier
    retourne un fichier et son objet transcripteur.
    """
    file = open(filePath, "w", newline='')
    writer = csv.writer(file)
    return (writer, file)

def close(file) :
    """
    Ferme le fichier "file"
    - file : le fichier a fermer
    """
    file.close()
    
def write(writer, data):
    '''
    Ecrit data dans le fichier ouvert par l'objet transcripteur "writer"
    - writer : l'objet transcripteur
    - data : le tableau à érire dans le fichier
    '''
    writer.writerow(data)
'''
===============================================
===============================================
'''



def caracterisation(lbp, vecSize):
    """
    Caracterise lbp par son histogramme.
    - lbp : le LBP d'une image (matrice).
    - vecSize : la taille du vecteur en sortie.
    Retourne : un vecteur de taille vecSize caracterisant 
    lbp (par son histogramme).
    """
    caract = []
    hist = np.histogram(lbp, bins=vecSize)
    # on caracterise le carreau avec son histogramme :
    for k in range(0,vecSize):
        caract = np.append(caract, str(hist[0][k]))
    return caract



def writeCaracterisation(imageMask, imageLbp, writer, vecSize):
    '''
    Ecrit dans le fichier filePath la caracterisation de tous 
    les rectangles de l'image dont le masque et le LBP sont 
    passes en parametres.
    - imageMask : le masque de l'image a caracteriser,
    comportant des 0 aux coordonnees ou l'image ne comporte
    pas de stries, et un nombre different de 0 ailleurs.
    - imageLbp : le LBP de l'image a caracteriser.
    - writer : l'objet transcripteur du fichier ou ecrire les caracterisations.
    - vecSize : la taille des vecteurs de caracterisation.
    '''
    surfaceRect = hRec*lRec
    for i in range(0,nbRecH) :
        for j in range(0,nbRecL) :
            surfaceRectMask = 0
            for k in range(0,hRec):
                for l in range(0,lRec):
                    if((np.shape(imageMask[i*hRec+k][j*lRec+l])==(2,) and 
                       imageMask[i*hRec+k][j*lRec+l][0]==0) or (np.shape(imageMask)==(1,) and 
                       imageMask[i*hRec+k][j*lRec+l]==0)):
                        surfaceRectMask = surfaceRectMask+1
            subLbp = imageLbp[i*hRec:(i+1)*hRec, j*lRec:(j+1)*lRec]
            
            if(surfaceRectMask/surfaceRect>0.3):
                caract = caracterisation(subLbp,vecSize)
                data = np.append(caract,str(1))
                write(writer, data)
            elif((i+j)%10 == 0):
                caract = caracterisation(subLbp,vecSize)
                data = np.append(caract,str(0))
                write(writer, data)
            '''
            caract = caracterisation(subLbp,vecSize)
            if(surfaceRectMask/surfaceRect>0.2):
                data = np.append(caract,str(1))
            else :
                data = np.append(caract,str(0))
            write(writer, data)
            '''




#from image import image
def main() :
    # chemin vers le fichier ou enregistrer la caracterisation :
    filePath = "caracTrainingSet.csv"
    # taille d'un vecteur caractérisant un sous rectangle
    vecSize = 28
    # image pour entrainer l'algorithme de machine learning :
    directoryImagePath = 'z_imagesPourMasques'
    imagesPath = os.listdir( directoryImagePath )
    imagesPath.sort()
    # image pour entrainer l'algorithme de machine learning :
    directoryMaskPath = 'z_masques'
    masksPath = os.listdir( directoryMaskPath )
    masksPath.sort()
    # application de writeCaracterisation sur toutes les images :
    (writer, file) = initWriter(filePath)
    for i in range(np.size(masksPath)):
        if((imagesPath[i].endswith('.tif') or imagesPath[i].endswith('.TIF')) and
        (masksPath[i].endswith('.tif') or masksPath[i].endswith('.TIF'))):
            print(directoryImagePath+"/"+imagesPath[i]+" : ")
            print(directoryMaskPath+"/"+masksPath[i]+" : ")
            '''
            imageTrain = image(directoryImagePath+"/"+imagesPath[i])
            imageMask = image(directoryMaskPath+"/"+masksPath[i])
            # calcul du LBP :
            imageLbp = imageTrain.LBP(n_points, radius)
            '''
            imageTrain = io.imread(directoryImagePath+"/"+imagesPath[i])
            imageTrain = resize(imageTrain, (imageTrain.shape[0]*scall, imageTrain.shape[1]*scall), mode='constant')
            imageMask = io.imread(directoryMaskPath+"/"+masksPath[i])
            imageMask = resize(imageMask, (imageMask.shape[0]*scall, imageMask.shape[1]*scall), mode='constant')
            # calcul du LBP :
            imageLbp = local_binary_pattern(imageTrain, n_points, radius, METHOD)
            
            
            # caracterisation de l'image :
            writeCaracterisation(imageMask, imageLbp, writer, vecSize)
            print(" OK ")
    close(file)

    
main()









