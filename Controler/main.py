from Model.SegmentationLBP import SegmentationLBP
import cv2
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
plt.figure(1)

##
# A ajouter à
##
imgRGB = Image.open("../Data/images/Stries_C2  (44).TIF")
img = cv2.imread("../Data/images/Stries_C2  (44).TIF",0)
imgRGB = cv2.imread("../Data/images/Stries_C2  (44).TIF",1)
sLBP = SegmentationLBP(img)
print(img.shape)
mask = sLBP.segmenterStriesLBP()
mask = mask*255
imgRGB[:,:,2] = mask
Image.fromarray(imgRGB).show()