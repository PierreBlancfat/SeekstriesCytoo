'''
Algorithme qui :
    - propose d'afficher quels sont les rectangles striés dans le dossier
    trainingImages. 
    - associe à chaque rectangle sa caractérisation
    - place dans un fichier : la caractérisation et un booleen (strié/non strié)
'''


import numpy as np
from Image import Image
import os
'''
Pour chaque image, on affiche le quadrillage et on propose à l'utilisateur de
cliquer sur les rectangles striés.
On ajoute alors cette donnée dans le fichier, associé a sa caractérisation.
''' 


######################################################################




'''
OPTIONS :
'''
# a priori, les options suivantes sont correctement calibrees :
nbRectHauteur = 32
nbRectLargeur = 24
scall = 1/2
# taille d'un vecteur caractérisant un sous rectangle
vecSize = 18

######################################################################


METHOD = 'uniform'

# settings for LBP
radius = 1
n_points = 8 * radius


# dimensions d'une image :
hImg = 1024*scall
lImg = 1344*scall
# nombre de rectangles :
nbRecH = int(nbRectHauteur*scall)
nbRecL = int(nbRectLargeur*scall)
# dimensions d'un rectangle :
hRec = int(hImg/nbRecH)
lRec = int(lImg/nbRecL)




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



from skimage import exposure

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
            pixelsBlancs = 0
            for k in range(0,hRec):
                for l in range(0,lRec):
                    if(imageMask.img[i*hRec+k][j*lRec+l]==0):
                        surfaceRectMask = surfaceRectMask+1
                    pixelsBlancs += (imageLbp[i*hRec+k][j*lRec+l]>1)
                    
                    
            subLbp = imageLbp[i*hRec:(i+1)*hRec, j*lRec:(j+1)*lRec]
            subLbp = exposure.equalize_hist(subLbp)
#            subLbp = exposure.adjust_sigmoid(subLbp)
#            subLbp = exposure.adjust_log(subLbp)

            if(surfaceRectMask/surfaceRect>0.2):
                caract = caracterisation(subLbp,vecSize)
                data = np.append(caract,str(1))
                write(writer, data)
            elif(surfaceRectMask==0 and pixelsBlancs>1500):
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



def main() :
    # chemin vers le fichier ou enregistrer la caracterisation :
    filePath = "caracTrainingSet.csv"
    # image pour entrainer l'algorithme de machine learning :
    directoryImagePath = 'images'
    imagesPath = os.listdir( directoryImagePath )
    imagesPath.sort()
    # image pour entrainer l'algorithme de machine learning :
    directoryMaskPath = 'training_masks'
    masksPath = os.listdir( directoryMaskPath )
    masksPath.sort()
    # application de writeCaracterisation sur toutes les images :
    (writer, file) = initWriter(filePath)
    for i in range(np.size(masksPath)):
        if(masksPath[i].endswith('_s.tif') or masksPath[i].endswith('_s.TIF')):
            for j in range(np.size(imagesPath)):
                if masksPath[i][:-6] in imagesPath[j]: 
                    print(directoryImagePath+"/"+imagesPath[j]+" : ")
                    print(directoryMaskPath+"/"+masksPath[i]+" : ")
                    print(directoryMaskPath+"/"+masksPath[i-1]+" : ")
            
                    imageTrain = Image(directoryImagePath+"/"+imagesPath[j], nbRecH = nbRecH, nbRecL = nbRecL)
                    imageMask = Image(directoryMaskPath+"/"+masksPath[i], nbRecH = nbRecH, nbRecL = nbRecL)
#                    imageMaskP = image(directoryMaskPath+"/"+masksPath[i-1])
                    
                    # ET logique pour fusionner le masque sur et le presque sur :
#                    imageMask.img = np.logical_and(imageMask.img, imageMaskP.img)
                    imageLbp = imageTrain.LBP(n_points, radius)

                    # caracterisation de l'image :
                    writeCaracterisation(imageMask, imageLbp, writer, vecSize)
                    print(" OK ")
    close(file)
    
main()









