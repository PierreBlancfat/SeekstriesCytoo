

##############################################################################
# Fonction de click sur une image utilisant Matplotlib et Numpy uniquement ###
##############################################################################


import numpy as np
import matplotlib.pyplot as plt



image = plt.imread('test.TIF') # Image to Array

fig = plt.figure()
ax = fig.add_subplot(111)
ax.imshow(image) # Affiche l'image sur le subplot

coords = []

def onclick(event):
    '''
    Fonction qui ajoute un event global
    @param event: l'event où sera stocké les coordonées
    @return: renvoie les coordonnées des cliques
    '''
    global ix, iy
    ix, iy = event.xdata, event.ydata
    print ('x = %d, y = %d'%(ix, iy))

    global coords
    coords.append((ix, iy))

    if len(coords) == 3: # limité à 2 cliques
        fig.canvas.mpl_disconnect(cid) # disconnect l'event cid

    return coords
cid = fig.canvas.mpl_connect('button_press_event', onclick) # crée un event cid sur la figure

plt.show()

##########################
# Clique to Matrix_index #
##########################

print(coords)

def clicksToIndex(coords):
    res = []
    # l = 1344
    # h = 1024
    # nb lignes = 32
    # nb colonnes = 24
    for i in range(len(coords)):
        res.append(( int(coords[i][0] % 32), int(coords[i][1] % 24) ))
    return res

print(int(17/32))
print(int(17/24))
print(clicksToIndex(coords))



