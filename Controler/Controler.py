from Model.Model import *
from View.View import *


class Controler():

    def __init__(self):
        frame = Tk()
        self.model = Model("a", "b")

        interface = Interface(frame)
        interface.mainloop()