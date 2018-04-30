
###########################
# SEGMENTATION DES FIBRES #
###########################

import numpy as np
import cv2
import scipy
import matplotlib.pyplot as plt

class SegmentationFibre:
    """
    Classe permettant de segment la fibre
    """

    def __init__(self, matImg):

        if (np.shape(np.shape(matImg))[0] > 2):
            self.matImg = cv2.cvtColor(matImg,cv2.COLOR_RGB2GRAY)
        else:
            self.matImg = matImg
        self.maskFibre = 0

    def segmenter(self):
        """
        Applique la methode des k-means sur une image pour la segmenter
        @param img: image a traiter (creer precedemment grace a "imread()")
        @return: l'image apres traitement
        """

        # k = 5, nombre de clusters optimal
        k = 5

        # convert to np.float32
        res = self.matImg.reshape((-1, 3))
        res = np.float32(res)

        # define criteria, number of clusters(K) and apply kmeans()
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
        ret, label, center = cv2.kmeans(res, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

        # Now convert back into uint8, and make original image
        center = np.uint8(center)
        res = center[label.flatten()]
        res = (res/np.min(res))-1 # normaliser a 0
        res = scipy.sign(res)
        maskFibre = res.reshape((self.matImg.shape))
        kernel = np.ones((20, 20), np.uint8)
        maskFibre = cv2.morphologyEx(maskFibre, cv2.MORPH_OPEN, kernel)
        self.maskFibre = maskFibre.astype(int)
        return maskFibre

'''
def main(): # Fonction de test
    plt.figure(1)
    img = cv2.imread('../Data/images/Stries_C2  (22).TIF')  #  Image de test
    plt.imshow(img)
    plt.figure(2)
    imgObj = SegmentationFibre(img)
    seg = imgObj.segmenter()
    plt.imshow(seg*255)
    plt.show()

main()
'''