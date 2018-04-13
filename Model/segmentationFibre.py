
###########################
# SEGMENTATION DES FIBRES #
###########################

import numpy as np
import cv2
import preTraitement

def fibreSegmentation(path):
    res = cv2.imread(path,0) # Image nuances de gris
    preTraitement.GB(res,1)
    preTraitement.HPF(res,1)
    return res

