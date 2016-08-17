from foil_view import View
from foil import Foil


class FoilController(object):
    def __init__(self):
        self.foil = Foil()
        self.view = View(self)

    def generateFoil(self):
        """ This is the recipient of the 'Generate foil' button event.
        Coordinates the generation of the foil profile, scales the point-set,
        and gets the view to draw it. """
        print "Generating the foil now..."

    def saveGcode(self):
        """ Triggered by the 'Save g-code' button event, it will coordinate
        production of the g-code for the displayed program passes and save it
        to files. """
        print "Saving the g-code now..."
