<h1 id="View.Interface">Interface</h1>

```python
Interface(self, controler, **kwargs)
```

Class holding the whole user interface of the application

<h2 id="View.Interface.changeCheckboxEntourage">changeCheckboxEntourage</h2>

```python
Interface.changeCheckboxEntourage(self)
```

Disable dest reposiory if we uncheck the box "Entourage"
:return:

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
Interface.displayImage(self, imageName, strie)
```

Display an image in its own size in a different window (on top level)
:param imageName: String that contains the imageName

<h2 id="View.Interface.createWindowStats">createWindowStats</h2>

```python
Interface.createWindowStats(self, clear, start)
```

Function linked to the Statistiques Window. It creates a whole new window on top of the main one. With details on the results, etc...
:param clear: Tells if we need to clean the window first
:param start: where to start in the list of images

<h2 id="View.Interface.saveCSV">saveCSV</h2>

```python
Interface.saveCSV(self)
```

A function that save the results in a CSV file at the root of the program

<h2 id="View.Interface.displayError">displayError</h2>

```python
Interface.displayError(self, message)
```

Display an error in a different window (on top level)
:param message: String that contains the error message

<h2 id="View.Interface.runProgressBar">runProgressBar</h2>

```python
Interface.runProgressBar(self)
```

Start the progress bar

<h2 id="View.Interface.stopProgressBar">stopProgressBar</h2>

```python
Interface.stopProgressBar(self)
```

Stop the progressbar at the end of processing

