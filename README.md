
# SeekStries
SeekStries is an image processing tool made with Python 3 which can find striations within muscular fibers images. 
Below an image example : 

<img src="https://i.imgur.com/mHUT2aY.jpg" width="400"/>

And a result :
<img src="https://i.imgur.com/mLUYgIF.png" width="400"/>


## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

 - Python 3.6 or later
 - Opencv
 - PIL
 - Tkinter
 - Scipy
 - Matplotlib


```bash
# List of commands (some will not work with Windows): 
pip3 install opencv-python
pip3 install Pillow
sudo apt-get install python3-tk
pip3 install scikit-image
```

### Installing

Clone Git repository (If you don't have any idea what's Git, check this website : http://rogerdudler.github.io/git-guide/)

> Run Controller with your IDE to launch the application

## Usage

<img src="https://i.imgur.com/v8jsrkw.png" width=500>

The software is in french so we will translate it line by line at the moment:
 - Save the images or not? If yes, it will be saved in two different repositories at the destination repository called "Stries/" and "nonStries/" depending on the fact that there are striations within the image or not.
 - Contouring? If yes, it puts a squared contouring around striations on top of the images
 - Select source repository
 - Select destination repository
After clicking "Start" button and the end of the execution, the "Stats" button will be available and will open this window:

<img src="https://i.imgur.com/yWbRQl2.png" width=800>

It allows you to check each percentages independently and open each images to see the concrete result.
You can save all the results in a *.csv and work with it later.

## Authors
This project was made by a group of students of UGA in France : 
Anouar Anasse, Pierre Blanc-Fatin, Vincent Ribot, Quentin Rospars and Yara Van Daalen. 
	
## Releases
V1.0.0 : Main functionalities


