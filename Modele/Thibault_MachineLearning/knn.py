# -*- coding: utf-8 -*-
"""
Created on Fri Apr 13 10:19:08 2018

@author: castellt
"""
import operator
import numpy as np
import math

class knn:
    
    def euclideanDistance(u, v):
        '''
        Retourne la distance euclidienne entre le vecteur u et v.
        - u et v deux vecteurs de même taille
        '''
        length = np.size(u)
        distance = 0
        for x in range(length-2):
            distance += pow((u[x] - v[x]), 2)
        return math.sqrt(distance)
    
        
    def getResponse(neighbors):
        classVotes = {}
        for x in range(len(neighbors)):
            response = neighbors[x][-1]
            if response in classVotes:
                classVotes[response] += 1
            else:
                classVotes[response] = 1
        sortedVotes = sorted(classVotes.items(), key=operator.itemgetter(1), reverse=True)
        return sortedVotes[0][0]
    
    
    def getNeighbors(reader, testInstance, k):
        '''
        Retourne les k voisins les plus proches du vecteur testInstance,
        parmi les vecteurs de trainingSet.
        '''
        distances = []
        for row in reader:
            row = list(map(int, row))
            dist = knn.euclideanDistance(testInstance, row)
            distances.append((row, dist))
        distances.sort(key=operator.itemgetter(1))
        neighbors = []
        for x in range(k):
            neighbors.append(distances[x][0])
        return neighbors