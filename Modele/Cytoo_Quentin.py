"""
===============================================
Local Binary Pattern for texture classification
===============================================

In this example, we will see how to classify textures based on LBP (Local
Binary Pattern). LBP looks at points surrounding a central point and tests
whether the surrounding points are greater than or less than the central point
(i.e. gives a binary result).

Before trying out LBP on an image, it helps to look at a schematic of LBPs.
The below code is just used to plot the schematic.
"""
from __future__ import print_function
import numpy as np
import matplotlib.pyplot as plt


METHOD = 'uniform'
plt.rcParams['font.size'] = 9

from skimage.transform import rotate
from skimage.feature import local_binary_pattern
from skimage import data
from skimage.color import label2rgb
from skimage import io
from scipy.spatial import distance as dist
import cv2

# settings for LBP
radius = 3
n_points = 8 * radius


def overlay_labels(image, lbp, labels):
    mask = np.logical_or.reduce([lbp == each for each in labels])
    return label2rgb(mask, image=image, bg_label=0, alpha=0.5)


def highlight_bars(bars, indexes):
    for i in indexes:
        bars[i].set_facecolor('r')
# x=530:y=600
# i=23 : j=38
image = cv2.imread('test.TIF',0)
plt.figure(0)
plt.imshow(image)
plt.figure(1)
lbp = local_binary_pattern(image, n_points, radius, METHOD)
lImg = 1344
hImg = 1024
lRec = int(lImg/24)
hRec = int(hImg/16)
nbRecH = int(hImg/hRec)
nbRecL = int(lImg/lRec)

plt.imshow(lbp)

#plt.imshow(lbp[hRec*9:hRec*10, lRec*9:lRec*10]) # LE CARRE A SELECTIONNER !
hist0 = cv2.calcHist(lbp, [0],None,[256],[0,256]) # L'histogramme du carre
plt.figure(2)
plt.plot(hist0)
'''
distRes = np.zeros((24,16))
def calcul(lbp):
    for i in range(0, nbRecL):
        for j in range(0, nbRecH):
            h0 = j * hRec
            l0 = i * lRec
            subRect = lbp[h0:h0 + hRec, l0:l0 + lRec]
            hist = cv2.calcHist(subRect, bins=26)
            #plt.plot(hist[1][0:25], hist[0][0:25])
            
            cv2.compareHist(hist, hist0, cv2.HISTCMP_CHISQR)
print(distRes)

def imgHist(path):
    image = io.imread(path)
    lbp = local_binary_pattern(image, n_points, radius, METHOD)
    hist = np.histogram(lbp, bins=26)
    plt.plot(hist[1][1:24],hist[0][1:24])
    return hist

calcul(lbp)
#print(dist.cityblock(hist[0][:],hist2[0][:]))

def hist(ax, lbp):
    n_bins = int(lbp.max() + 1)
    return ax.hist(lbp.ravel(), normed=True, bins=n_bins, range=(0, n_bins), facecolor='0.5')
'''
'''
# plot histograms of LBP of textures
fig, (ax_img, ax_hist) = plt.subplots(nrows=2, ncols=3, figsize=(9, 6))
plt.gray()

titles = ('edge', 'flat', 'corner')
w = width = radius - 1
edge_labels = range(n_points // 2 - w, n_points // 2 + w + 1)
flat_labels = list(range(0, w + 1)) + list(range(n_points - w, n_points + 2))
i_14 = n_points // 4            # 1/4th of the histogram
i_34 = 3 * (n_points // 4)      # 3/4th of the histogram
corner_labels = (list(range(i_14 - w, i_14 + w + 1)) +
                 list(range(i_34 - w, i_34 + w + 1)))

label_sets = (edge_labels, flat_labels, corner_labels)

for ax, labels in zip(ax_img, label_sets):
    ax.imshow(overlay_labels(image, lbp, labels))

for ax, labels, name in zip(ax_hist, label_sets, titles):
    counts, _, bars = hist(ax, lbp)
    highlight_bars(bars, labels)
    ax.set_ylim(ymax=np.max(counts[:-1]))
    ax.set_xlim(xmax=n_points + 2)
    ax.set_title(name)

ax_hist[0].set_ylabel('Percentage')
for ax in ax_img:
    ax.axis('off')


######################################################################
# The above plot highlights flat, edge-like, and corner-like regions of the
# image.
#
# The histogram of the LBP result is a good measure to classify textures.
# Here, we test the histogram distributions against each other using the
# Kullback-Leibler-Divergence.
'''
plt.show()
