"""
This example module shows various types of documentation available for use
with pydoc.  To generate HTML documentation for this module issue the
command:

    pydoc -w foo

"""

###########################
# SEGMENTATION DES FIBRES #
###########################

import numpy as np
import cv2
import scipy

class SegmentationFibre:
    """
    Classe permettant de segment la fibre
    """

    def __init__(self, matImg):

        self.matImg = matImg
        self.maskFibre = 0

    def segmenter(self, img,k):
        """
        Applique la methode des k-means sur une image pour la segmenter
        @param img: image a traiter (creer precedemment grace a "imread()")
        @return: l'image apres traitement
        """

        # k = 5, nombre de clusters optimal
        k = 5

        # convert to np.float32
        res = img.reshape((-1, 3))
        res = np.float32(res)

        # define criteria, number of clusters(K) and apply kmeans()
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
        ret, label, center = cv2.kmeans(res, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

        # Now convert back into uint8, and make original image
        center = np.uint8(center)
        res = center[label.flatten()]
        res = (res/np.min(res))-1 # normaliser a 0
        res = scipy.sign(res)
        maskFibre = res.reshape((img.shape))
        self.maskFibre = maskFibre
        return maskFibre

    '''
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
    '''