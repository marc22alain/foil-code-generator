from naca_00 import NACA_00
from naca_63 import NACA_63



class Foil(object):
	def __init__(self):
		# assign the default foil formula
		self.formula = NACA_00()
		# assign the (default) truncation type: None should produce a square end
		self.truncation = None
		# assign the (default) width where the transition occurs
		self.transition = 0
		self.point_set = None

	def setFormula(self, formula):
		""" User may decide to change the profile formula for their foil. """
		if formula == "NACA-00":
			self.formula = NACA_00()
		elif formula == "NACA-63":
			self.formula == NACA_63()

	def generatePointSet(self, parameters):
		""" Triggered by the 'Generate foil' button, this will calcuate the
		full set of points on the foil profile according the parameters chosen
		by the user. """
		self.width = parameters["width"]
		self.thickness = parameters["thickness"]
		self.rad_tolerance = parameters["rad_tolerance"]
		self.max_chine = parameters["max_chine"]
		self.regime_split = parameters["regime_split"]
		# TODO: do a whole lot of calculations !
		return self.point_set
