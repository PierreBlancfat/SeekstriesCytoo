<h1 id="View.Interface">Interface</h1>

```python
Interface(self, controler, **kwargs)
```

Class holding the whole user interface of the application

<h2 id="View.Interface.browseRepSrc">browseRepSrc</h2>

```python
Interface.browseRepSrc(self)
```

Allows to change the source repository
:return: none

<h2 id="View.Interface.browseRepDest">browseRepDest</h2>

```python
Interface.browseRepDest(self)
```

Allow to change the destination repository
:return: none

<h2 id="View.Interface.cliquer">cliquer</h2>

```python
Interface.cliquer(self)
```

Launch the program itself

<h2 id="View.Interface.pause">pause</h2>

```python
Interface.pause(self)
```

Pause the program during its execution

<h2 id="View.Interface.changeState">changeState</h2>

```python
Interface.changeState(self)
```

Allows to unlock Stats tab after the execution

<h2 id="View.Interface.displayImage">displayImage</h2>

```python
Interface.displayImage(self, imageName)
```

Display an image in its own size in a different window (on top level)
:param imageName: String that contains the imageName

<h2 id="View.Interface.createWindowStats">createWindowStats</h2>

```python
Interface.createWindowStats(self)
```

Function linked to the Statistiques Window. It creates a whole new window on top of the main one. With details on the results, etc...

<h2 id="View.Interface.saveCSV">saveCSV</h2>

```python
Interface.saveCSV(self)
```

A function that save the results in a CSV file at the root of the program

