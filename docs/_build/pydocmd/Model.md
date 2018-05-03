<h1 id="Area.Area">Area</h1>

```python
Area(self, xTopLeft, yTopLeft, xBotRight, yBotRight)
```

<h2 id="Area.Area.border">border</h2>

list() -> new empty list
list(iterable) -> new list initialized from iterable's items
<h2 id="Area.Area.expend">expend</h2>

```python
Area.expend(self, x, y)
```

expend the current area if the position of the pixel is out of the area
:param x: abscissa coordinate of the pixel
:param y: ordinate coordonate of the pixel
:return: None

<h2 id="Area.Area.equals">equals</h2>

```python
Area.equals(self, area)
```
indicate if the current area is equal to the area in parameter.

:param area: the area which may be equal to the current area
:type area: list
:return: True if the current area is equal to the area in parameter, false else.
:rtype: bool

<h2 id="Area.Area.notContainedIn">notContainedIn</h2>

```python
Area.notContainedIn(self, area)
```
indicate if the current area is not contained in the area in parameter.

:param area: the area which may contain the current area
:type area: list
:return: True if the current area is not contained in the area in parameter, false else.
:rtype: bool

<h2 id="Area.Area.notToSmall">notToSmall</h2>

```python
Area.notToSmall(self, minWidth, minHeight)
```
indicate if the current area isn't to small.

:param minWidth: the minimal width for an area to be considered.
:type minWidth: int
:param minHeight: the minimal height for an area to be considered.
:type minHeight: int
:return: True if the current area isn't to small, false else.
:rtype: bool

<h1 id="Model.Model">Model</h1>

```python
Model(self, repSource, repDestination, controler)
```

<h2 id="Model.Model.setRepSource">setRepSource</h2>

```python
Model.setRepSource(self, repSource)
```

set the source directory
:param repSource: the path of the source repertory
:type str
:return:

<h2 id="Model.Model.setRepDestination">setRepDestination</h2>

```python
Model.setRepDestination(self, repDestination)
```

Set the destination directory. Create a directory if it doesn't exist
:param repDestination: path of the destination directory
:return:

<h2 id="Model.Model.SegmentationUneImage">SegmentationUneImage</h2>

```python
Model.SegmentationUneImage(self, nomImg)
```

Do the segmentation of one image, save it if users want to, put the bording boxes if the users want to.
:param nomImg: Name of the image to segmentate
:type a matrix which represent an image
:return:

<h2 id="Model.Model.runSegmentation">runSegmentation</h2>

```python
Model.runSegmentation(self, cbEntourage, otherRep)
```

Action of the start bouton, product threads in order to speed up the computation
Product threah
:param cbEntourage: CheckBox entourage value
:type cbEntourage : IntVar
:param otherRep: Checkbox save in an path
:type otherRep : IntVar
:return: 0 when segmentation is finished

<h2 id="Model.Model.multipleImage">multipleImage</h2>

```python
Model.multipleImage(self, nomsImages)
```

Method run in a thread, call segmentationUneImage fonction for each in the list of images in parameter
:param nomsImages: a list of image name
:type str
:return:

<h2 id="Model.Model.normalizePath">normalizePath</h2>

```python
Model.normalizePath(self, s)
```

Normalize a path to be compatible with windows
:param s: a path
:type str
:return: s normalized

<h2 id="Model.Model.finDeTraitement">finDeTraitement</h2>

```python
Model.finDeTraitement(self)
```

Executed when a segmentation is finished, unlock stat bouton
:return:

<h1 id="Segmentation.Segmentation">Segmentation</h1>

```python
Segmentation(self, cheminSrc, cheminDest)
```

Classe qui permet d'appeler les deux segmentations et calcul la proportion de stries dans une image

<h2 id="Segmentation.Segmentation.segmenterUneImage">segmenterUneImage</h2>

```python
Segmentation.segmenterUneImage(matImg)
```

Segmente une image (fibre et stries)
:param matImg: une image sous forme de matrice
:return: les deux masques des segmentations

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

<h2 id="SegmentationGabor.SegmentationGabor.gabor">gabor</h2>

```python
SegmentationGabor.gabor(self, imgG, csize, lsize, thetaMin, thetaMax, pasTheta, sigma, gamma, lambdaMin, lambdaMax, pasLambda, psi)
```

Main fonction, call buildfilter anc process
:return:

<h2 id="SegmentationGabor.SegmentationGabor.build_filters">build_filters</h2>

```python
SegmentationGabor.build_filters(self, csize, lsize, thetaMin, thetaMax, pasTheta, sigma, gamma, lambdaMin, lambdaMax, pasLambda, psi)
```

Builds gabor filter
:return: A list with the gabor filter

<h2 id="SegmentationGabor.SegmentationGabor.process">process</h2>

```python
SegmentationGabor.process(self, img, filters)
```

Convolution of each gabor filter
:param img: a matrix which represents a picture
:param filters: a list of matrix which represents gabor filters
:return: The response of the convolution

<h2 id="SegmentationGabor.SegmentationGabor.segmentation">segmentation</h2>

```python
SegmentationGabor.segmentation(self)
```

Segmentation of a image
:param matImg: a matrix which reresents an image
:return: a mask which represent the segmentation. 1 means the algorithm detect a striation,

<h2 id="SegmentationGabor.SegmentationGabor.conversionBinaire">conversionBinaire</h2>

```python
SegmentationGabor.conversionBinaire(self, img)
```

Convert a matrix into a binary matrix
 :param img: a int matrix
 :return: a binary matrix

<h2 id="SegmentationGabor.SegmentationGabor.inverseMatBin">inverseMatBin</h2>

```python
SegmentationGabor.inverseMatBin(self, mat)
```

Create the inverse of a binary matrix, 0 become 1, 1 become 0
:param mat: a binary matrix
:return: a binary matrix

<h2 id="SegmentationGabor.SegmentationGabor.kMeans">kMeans</h2>

```python
SegmentationGabor.kMeans(img, k)
```

Applique la méthode des k-means sur une image pour la segmenter
@param img: image à traiter (créer précédemment grâce à "imread()")
@param k: nombre de clusters
@return: l'image après traitement

