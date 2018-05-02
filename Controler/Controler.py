from View.View import *
from Model.Model import *

class Controler():

    def __init__(self):
        self.model = Model("a", "b")
        self.interface = Interface(self)
        self.interface.configure(background='#323232')
        self.interface.minsize(550,350)
        self.interface.mainloop()


    def segmentation(self):
        """"
        Main function which execute the whole code
        :param entourage: 0 or 1 if the user wants a contouring or not
        :param otherRep: 0 or 1 if the user wants to separate image  with striations
        :return:
        """
        #Gestion des erreur
        print(self.interface.champsRepDest.get())
        if self.interface.champsRepDest.get() == "" and self.interface.entourage.get() == 1:
            self.interface.displayError("Le chemin de destination est vide")
        elif (self.interface.champsRepSource.get() == ""):
            self.interface.displayError("Le chemin source est vide")
        else:
            try:
                valueReturned = self.model.runSegmentation(self.interface.entourage,self.interface.otherRep)
            except FileNotFoundError as errCheminIntrouvble:
                self.interface.displayError("Chemin introuvable : "+errCheminIntrouvble.filename)
            if (valueReturned == 0):
                self.interface.changeState()

    def testEntourage(self):
        print("a faire depuis le Model directement")
        #self.model.saveEntourage() call this function in the model object

    def giveRepPath (self, repSource, repDest) :
        self.model.setRepSource(repSource)
        self.model.setRepDestination(repDest)


if __name__ == '__main__':
    Controler()
