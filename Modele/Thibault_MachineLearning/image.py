# -*- coding: utf-8 -*-
"""
Created on Fri Apr 13 10:20:57 2018

@author: castellt
"""
from skimage.feature import local_binary_pattern
from skimage.transform import resize
from skimage import io
from skimage.viewer import ImageViewer
import numpy as np

class image:

    def __init__(self, path, **keys):
        '''
        Parametres :
            
            - path (obligatoire) : chemin
            - resize : booleen, si false l'image n'est pas redimensionnee
            (par defaut, resize = true)
            - hauteur : hauteur de l'image (avant resize)
            - largeur : largeur de l'image (avant resize)
            - scall : ratio de redimensionnement de l'image
                
        Exemples :
            
            - image(path) : 
                image par défaut ((1024*0.5)*(1344*0.5))
            
            - image(path, resize) : 
                image par défaut non redimensionnée si
                resize est false ((1024)*(1344))
            
            - image(path, hauteur, largeur) :
                image de dim ((hauteur*0.5)*(largeur*0.5))
            
            - image(path, hauteur, largeur, scall) : 
                image de dim ((hauteur*scall)*(largeur*scall))
            
            - image(path, scall) : 
                image par défaut redimensionnée, de
                dim ((1024*scall)*(1344*scall)
        '''        
        # echelle pour la redimension :
        if 'resize' in keys and (keys['resize'] == False):
            self.scall = 1
        elif 'scall' in keys: self.scall = keys['scall']
        else : self.scall = 1/2
        
        # dimensions d'une image :
        if 'hauteur' in keys: self.hImg = keys['hauteur']*self.scall
        else : self.hImg = 1024*self.scall
        
        if 'largeur' in keys: self.lImg = keys['largeur']*self.scall
        else : self.lImg = 1344*self.scall
        

        # nombre de rectangles :
        self.nbRecH = int(32*self.scall)
        self.nbRecL = int(24*self.scall)
        # dimensions d'un rectangle :
        self.hRec = int(self.hImg/self.nbRecH)
        self.lRec = int(self.lImg/self.nbRecL)
        
        self.img = io.imread(path)
        if 'resize' in keys and (keys['resize'] == True):
            self.img = resize(self.img, (self.img.shape[0]*self.scall, self.img.shape[1]*self.scall), mode='constant')



    def LBP(self, n_points, radius):
        return local_binary_pattern(self.img, n_points, radius, 'uniform')
        
    
    
    def colorResult(self, setOut):
        '''
        code pour coloriser les sous rectangles sriés.
        '''
        
        x = np.shape(setOut)[1]
        y = np.shape(setOut)[0]
        rx = int(self.nbRecL/x)
        ry = int(self.nbRecH/y)
        
        for i in range(y) :
            for j in range(x) :
                if(setOut[i][j]==1):
                    for k in range(0,self.hRec):
                        l = np.arange(0, self.lRec)
                        self.img[i*rx*self.hRec+k][j*ry*self.lRec+l] += 7000



      
        
    def display(self):
        return ImageViewer(self.img)






