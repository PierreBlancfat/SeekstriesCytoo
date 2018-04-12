

########################################################################################
#                                                                                      #
# Script pour faire un pré-traitement sur les images avant d'appliquer nos algorithmes #
#                                                                                      #
########################################################################################

import matplotlib.pyplot as plt
import numpy as np
import cv2


img = cv2.imread('test.TIF',0)
# cv2.imshow('Fibre musculaire', img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()


# Low-pass filters aide à réduire le bruit
LPF1 = np.ones((3,3),np.float32)/9
LPF2 = np.ones((5,5),np.float32)/50


# High-pass filters aide à trouver les edges dans une image
HPF1 = -1*np.ones((5,5))
HPF1[3][3] = 25


img_LPF1 = cv2.filter2D(img,-1,LPF1)
img_LPF2 = cv2.filter2D(img,-1,LPF2)
img_HPF1 = cv2.filter2D(img,-1,HPF1)
img_GB1  = cv2.GaussianBlur(img,(5,5),0)

# Bilateral filters is highly effective in noise removal while keeping edges sharp
img_BLF = blur = cv2.bilateralFilter(img,5,75,75)


plt.subplot(121)
plt.imshow(img)
plt.subplot(122)
plt.imshow(img_BLF)
plt.show()
