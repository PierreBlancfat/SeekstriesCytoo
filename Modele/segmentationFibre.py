
###########################
# SEGMENTATION DES FIBRES #
###########################

import numpy as np
import matplotlib.pyplot as plt
import cv2
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

    # Enlever les bout "seuls"
    kernel = np.ones((30, 30), np.uint8)
    res2 = cv2.morphologyEx(res2, cv2.MORPH_OPEN, kernel)
    return res2

def contourFibre(img):
    '''
    Trouve le contour de la fibre
    :param img: image (faite avec imread(chemin, 1)
    :return: nouvelle image avec le contour dessus
    '''
    ret, thresh = cv2.threshold(img, 127, 255, 0)
    thresh = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY);
    im2, contours, hierarchy = cv2.findContours(thresh, 1, 2)
    cnt = contours[0]
    rect = cv2.minAreaRect(cnt)
    box = cv2.boxPoints(rect)
    box = np.int0(box)
    img = cv2.drawContours(img, [box], 0, (0, 0, 255), 2)

    return img

def main(): # Fonction de test
    start_time = time.time()

    plt.figure(1)
    plt.subplot(121)
    img = cv2.imread('ImagesTests/Quentin/Stries_C2  (144).tif', 0)
    plt.imshow(img)
    plt.subplot(122)
    imgSeg = kMeans(cv2.imread('ImagesTests/Quentin/Stries_C2  (144).tif',0),5)
    cv2.imwrite('ImagesTests/Quentin/Stries_C2  (144)_SegFibre.tif', imgSeg)
    plt.imshow(imgSeg)

    plt.figure(2)
    imgCont = cv2.imread('ImagesTests/Quentin/Stries_C2  (144)_SegFibre.tif', 1)
    imgCont = contourFibre(imgCont)
    plt.imshow(imgCont)


    print("--- %s seconds ---" % (time.time() - start_time))
    plt.show()

main()