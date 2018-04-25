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

class Image:

    def __init__(self, **keys):
        '''
        Parametres :
            
            - path : chemin (pas compatible avec le parametre matrix)
            - matrix : numpy matrice représentant l'image (pas compatible avec le parametre path)
            - resize : booleen, si false l'image n'est pas redimensionnee
            (par defaut, resize = true)
            - hauteur : hauteur de l'image (avant resize)
            - largeur : largeur de l'image (avant resize)
            - scall : ratio de redimensionnement de l'image
                
        Exemples :
            - image(matrix):
                image par défaut ((1024*0.5)*(1344*0.5))
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
        if 'nbRecH' in keys :
            self.nbRecH = int(keys['nbRecH']*self.scall)
        else:
            self.nbRecH = 32*self.scall
        if 'nbRecL' in keys :
            self.nbRecL = int(keys['nbRecL']*self.scall)
        else:
            self.nbRecL = 24*self.scall

        # dimensions d'un rectangle :
        self.hRec = int(self.hImg/self.nbRecH)
        self.lRec = int(self.lImg/self.nbRecL)
        
        if ('path' in keys) and ('matrix' in keys) :
            print("ERREUR : les parametres path et matrix sont incompatibles")
        elif (not 'path' in keys) and (not 'matrix' in keys) :
            print("ERREUR : l'un des parametres suivant est necessaire : path, matrix")
        elif ('path' in keys) :
            self.img = io.imread(keys['path'])
        else :
            self.img = keys['matrix']
        
        if(len(self.img.shape)==3):
            self.img = self.img[:,:,0]
            
        if not('resize' in keys) or ('resize' in keys and (keys['resize'] == True)):
            self.img = resize(self.img, (self.img.shape[0]*self.scall, self.img.shape[1]*self.scall), mode='constant')


    def LBP(self, n_points, radius):
        return local_binary_pattern(self.img, n_points, radius, 'uniform')
        
    
    
    def colorResult(self, setOut, scall):
        '''
        code pour coloriser les sous rectangles striés.
        '''

        x = np.shape(setOut)[1]
        y = np.shape(setOut)[0]
        
        if(self.scall == 1): antiscall = 1
        else : antiscall = int(1/scall)
        
        for i in range(y) :
            for j in range(x) :
                if(setOut[i][j]==1):
                    for k in range(0,self.hRec*antiscall):
                        for l in range(0,self.lRec*antiscall):
                            if(self.img[i*self.hRec*antiscall+k][j*self.lRec*antiscall+l]>6000):
                                self.img[i*self.hRec*antiscall+k][j*self.lRec*antiscall+l] += 8000

    def returnMask(self, setOut, scall):
        '''
        code pour renvoyer le masque des sous rectangles striés.
        '''
        mask = np.zeros(self.img.shape)
        x = np.shape(setOut)[1]
        y = np.shape(setOut)[0]

        if (self.scall == 1):
            antiscall = 1
        else:
            antiscall = int(1 / scall)

        for i in range(y):
            for j in range(x):
                if (setOut[i][j] == 1):
                    for k in range(0, self.hRec * antiscall):
                        for l in range(0, self.lRec * antiscall):
                            if (self.img[i * self.hRec * antiscall + k][j * self.lRec * antiscall + l] > 6000):
                                mask[i * self.hRec * antiscall + k][j * self.lRec * antiscall + l] = 1
                            else :
                                mask[i * self.hRec * antiscall + k][j * self.lRec * antiscall + l] = 0
        return mask

    def display(self):
        return ImageViewer(self.img)






