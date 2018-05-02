<h1 id="Area.Area">Area</h1>

```python
Area(self, xTopLeft, yTopLeft, xBotRight, yBotRight)
```

<h2 id="Area.Area.border">border</h2>

list() -> new empty list
list(iterable) -> new list initialized from iterable's items
<h1 id="EvaluationSegmentation.EvaluationSegmentation">EvaluationSegmentation</h1>

```python
EvaluationSegmentation(self, srcDossierImageRef, srcDossiertest, algoSegmentation)
```

<h2 id="EvaluationSegmentation.EvaluationSegmentation.evalUneImage">evalUneImage</h2>

```python
EvaluationSegmentation.evalUneImage(self, imgRef, imgTest)
```

Evaluation de la qualité d'une segmentation
:param imgRef: une matrice binaire
:param nomImgTest: une matrice binaire
:return: [precision,prevalence,PPV,FDR,FOR,NPV,TPR,FPR,FNR,TNR,LRplus,LRmoins,vraivrai]

<h2 id="EvaluationSegmentation.EvaluationSegmentation.evalDesImages">evalDesImages</h2>

```python
EvaluationSegmentation.evalDesImages(self, algoSegmentation)
```

:param srcRef: chemin du dossier reference ( masque binaire)
:param srcTest:v chemin du dossier des images test
:return: une matrice avec autant de lignes que d'images

<h2 id="EvaluationSegmentation.EvaluationSegmentation.conversionBinaire">conversionBinaire</h2>

```python
EvaluationSegmentation.conversionBinaire(self, img)
```

Convertie une image en binaire
:param srcImageRef: Le chemin de l'image
:return: Une matrice binaire de même taille que l'image source. Les 1 représentent le "noir" ( zone positive), le 0 le "blanc" ( zone négative)

<h2 id="EvaluationSegmentation.EvaluationSegmentation.concatMasque">concatMasque</h2>

```python
EvaluationSegmentation.concatMasque(self, masque1, masque2)
```

Concatène des masques binaires
:param masque1: une matrice binaire
:param masque2: une matrice binaire
:return: (masque1 & masque2)

<h1 id="Model.Model">Model</h1>

```python
Model(self, repSource, repDestination)
```

<h1 id="Segmentation.Segmentation">Segmentation</h1>

```python
Segmentation(self, cheminSrc, cheminDest)
```

<h2 id="Segmentation.Segmentation.propStries">propStries</h2>

```python
Segmentation.propStries(masqueFibre, masqueStries)
```

Calcul la proportion de stries dans une fibre
:param masqueFibre: une matrice binaire
:param masqueStries: une matrice binaire
:return: proportion des stries dans la fibre

<h1 id="SegmentationFibre.SegmentationFibre">SegmentationFibre</h1>

```python
SegmentationFibre(self, matImg)
```

Classe permettant de segmenter la fibre

<h2 id="SegmentationFibre.SegmentationFibre.segmenter">segmenter</h2>

```python
SegmentationFibre.segmenter(self)
```

Applique la methode des k-means sur une image pour la segmenter
@param img: image a traiter (creer precedemment grace a "imread()")
@return: l'image apres traitement

<h1 id="SegmentationGabor.SegmentationGabor">SegmentationGabor</h1>

```python
SegmentationGabor(self, matImg, csize=50, lsize=50, thetaMin=-0.4, thetaMax=0.45, pasTheta=0.2, sigma=2, gamma=5, lambdaMin=6, lambdaMax=15, pasLambda=2, psi=0, dossierSaveImgSeg=None, dossierSaveKernel=None)
```

<h2 id="SegmentationGabor.SegmentationGabor.kMeans">kMeans</h2>

```python
SegmentationGabor.kMeans(img, k)
```

Applique la méthode des k-means sur une image pour la segmenter
@param img: image à traiter (créer précédemment grâce à "imread()")
@param k: nombre de clusters
@return: l'image après traitement

<h2 id="SegmentationGabor.SegmentationGabor.conversionBinaire">conversionBinaire</h2>

```python
SegmentationGabor.conversionBinaire(selg, img)
```

Convertie une image en binaire
:param srcImageRef: Le chemin de l'image
:return: Une matrice binaire de même taille que l'image source. Les 1 représentent le "noir" ( zone positive), le 0 le "blanc" ( zone négative)

<h2 id="SegmentationGabor.SegmentationGabor.segmentation">segmentation</h2>

```python
SegmentationGabor.segmentation(self)
```

Segmente une image avec les filtres de Gabor
:param matImg: un emtrice représentant une image
:return: Le masque représentant la segmentation

