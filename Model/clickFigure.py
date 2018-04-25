

##############################################################################
# Fonction de click sur une images utilisant Matplotlib et Numpy uniquement ###
##############################################################################


import numpy as np
import matplotlib.pyplot as plt



image = plt.imread('test.TIF') # Image to Array

fig = plt.figure()
ax = fig.add_subplot(111)
ax.imshow(image) # Affiche l'images sur le subplot

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



