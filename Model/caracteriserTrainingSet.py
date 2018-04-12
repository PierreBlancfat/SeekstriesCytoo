'''
Algorithme qui :
    - propose d'afficher quels sont les rectangles striés dans le dossier
    trainingImages. 
    - associe à chaque rectangle sa caractérisation
    - place dans un fichier : la caractérisation et un booleen (strié/non strié)
'''
import csv
from skimage.feature import local_binary_pattern
from skimage import io
import numpy as np

'''
Pour chaque image, on affiche le quadrillage et on propose à l'utilisateur de
cliquer sur les rectangles striés.
On ajoute alors cette donnée dans le fichier, associé a sa caractérisation.
''' 

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D 
import matplotlib.patches as patches

METHOD = 'uniform'
plt.rcParams['font.size'] = 9

# settings for LBP
radius = 3
n_points = 8 * radius

# dimensions d'une image :
hImg = 1024
lImg = 1344
# dimensions d'un rectangle :
hRec = int(hImg/32)
lRec = int(lImg/24)
# nombre de rectangles :
nbRecH = int(hImg/hRec)
nbRecL = int(lImg/lRec)

# taille d'un vecteur caractérisant un sous rectangle
vecSize = 28


def caracterisation(lbp):
    """
    Caracterise les sous rectangles de lbp par les histogrammes
    de ces sous rectangles, et place ces caractéristiques dans la
    matrice set.
    """
    caract = []
    hist = np.histogram(lbp, bins=vecSize)
    # on caracterise le carreau avec son histogramme :
    for k in range(0,vecSize):
        caract = np.append(caract, str(hist[0][k]))
    return caract



def colorRect(i,j,ax):
    ax.add_patch(
        patches.Rectangle(
            (i*lRec, j*hRec),   # (x,y)
            lRec,          # width
            hRec,          # height
            alpha = 0.35,   # transparence
            color = "red"
        )
    )




def rectanglesAcquisition(imagePath, lbp) :
    """ Mouse acquisition of rectangles
        right click to stop
    """
    
    fname = "caracTrainingSet.csv"

    file = open(fname, "w")
    writer = csv.writer(file)

    fig = plt.figure()
    ax = fig.add_subplot(111)
    img = plt.imread(imagePath)
    for i in range(nbRecH) :
        n = i*hRec
        l = Line2D([0,lImg],[n,n])                             
        ax.add_line(l) 
    for i in range(nbRecL) :
        n = i*lRec
        l = Line2D([n,n],[0,hImg])                                    
        ax.add_line(l)
    
    ax.imshow(img)
    coord = 0
    while coord != []:
        coord = plt.ginput(1, mouse_add=1, mouse_stop=3, mouse_pop=2)
        # coord is a list of tuples : coord = [(x,y)]
        if coord != []:
            xx = coord[0][0]
            yy = coord[0][1]
            i = int(xx/lRec)
            j = int(yy/hRec)
            colorRect(i, j, ax)
            plt.draw()
            subLbp = lbp[i*lRec:(i+1)*lRec, j:(j+1)*lRec]
            caract = caracterisation(subLbp)
            writer.writerow( np.append(caract,str(1)) )
    file.close()

def main() :
    # image pour entrainer l'algorithme de machine learning :
    imagePath = 'test.tif'
    imageTrain = io.imread(imagePath)
    lbpTrain = local_binary_pattern(imageTrain, n_points, radius, METHOD)
    rectanglesAcquisition(imagePath, lbpTrain)
    
    
main()


'''
 après clique droit, ajouter toutes les autres cases en
 non striées puis passage à l'image suivante (ou fin du programme
 si plus d'images à parcourir)
'''






