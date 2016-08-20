from foil_view import View
from foil import Foil
from foil_menubar import MenuBar


class FoilController(object):
    def __init__(self):
        self.foil = Foil()
        self.view = View(self)
        self.menu = MenuBar(self, self.view)

    def generateFoil(self):
        """ This is the recipient of the 'Generate foil' button event.
        Coordinates the generation of the foil profile, scales the point-set,
        and gets the view to draw it. """
        print "Generating the foil now..."
        self.point_set = self.foil.generatePointSet(self.view.getFoilParameters())
        self.view.drawFoil(self.point_set)



    def saveGcode(self):
        """ Triggered by the 'Save g-code' button event, it will coordinate
        production of the g-code for the displayed program passes and save it
        to files. """
        print "Saving the g-code now..."

    def chooseNACA_00(self):
        pass

    def chooseNACA_63(self):
        pass