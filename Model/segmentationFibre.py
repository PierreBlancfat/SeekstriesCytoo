
###########################
# SEGMENTATION DES FIBRES #
###########################

import numpy as np
import matplotlib.pyplot as plt
import cv2
import preTraitementImg
import time
import scipy


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
    res = scipy.sign(res) # Binarisation
    res = res * 255 # pour afficher en noir blanc
    res2 = res.reshape((img.shape))

    return res2

def main(): # Fonction de test
    start_time = time.time()

    plt.figure(1)
    plt.subplot(121)
    img = cv2.imread('Stries_C2  (11).TIF', 0)
    plt.imshow(img)
    plt.subplot(122)
    #imgSeg = fibreSegmentation('Stries_C2  (22).TIF')
    imgSeg = kMeans(cv2.imread('Stries_C2  (11).TIF',0),5)
    plt.imshow(imgSeg)

    plt.figure(2)
    plt.hist(img.ravel(),bins='auto')


    print("--- %s seconds ---" % (time.time() - start_time))
    plt.show()

# main()