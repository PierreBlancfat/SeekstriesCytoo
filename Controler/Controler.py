from View.View import *
from Model.Segmentation import Segmentation


frame = Tk()


def initFenetre():
    label = Label(frame, text="Hello World")
    interface = Interface(frame)
    interface.mainloop()



if __name__ == '__main__':
    initFenetre()
