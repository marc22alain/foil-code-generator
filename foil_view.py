from Tkinter import *
import ttk
from math import *

import os
import sys

# This app is designed to be co-located with the G-code-repositories
# START for local module imports:
path = os.getcwd().split("/")
# print path

new_path = ""
for i in xrange(1, len(path) - 1):
    new_path += "/" + path[i]
new_path += "/" + "G-code-repositories"
# print new_path

sys.path.append(new_path)


import Glib as G
import MC_defaults as MC
import simple_generators as SG
# END for local module imports:


class View(Tk):
    """ The View holds the ttk.Notebook and its multiple tabs. """
    def __init__(self, controller, master=None):
        Tk.__init__(self)
        self.controller = controller
        self.notebook = ttk.Notebook()
        self.foil_view = FoilView(self.controller, self)
        self.stock_view = StockView(self.controller, self)
        self.notebook.add(self.foil_view, text='Foil definition')
        self.notebook.add(self.stock_view, text='Stock definition')
        self.notebook.pack(expand=1, fill="both")

    def getFoilParameters(self):
        parameters = {"width": self.foil_view.section_width_var.get(),
                      "thickness": self.foil_view.section_thickness_var.get(),
                      "rad_tolerance": self.foil_view.radians_tolerance_var.get(),
                      "max_chine": self.foil_view.max_chine_length_var.get(),
                      "regime_split": self.foil_view.regime_split_var.get()}
        return parameters

    def drawFoil(self, point_set):
        # TODO: figure out how to to decide between length-wise or cross-wise drawing
        # self.foil_view.drawFoilChined(point_set)
        self.foil_view.drawFoilPoints(point_set)


    def getStockParameters(self):
    	pass



class TabView(Frame):
    """ The parent for StockView and FoilView Frame(s), holding attributes and
    behaviour in common. """
    def __init__(self, controller, master=None):
        self.scale = 700
        self.translate_X = 55
        self.translate_Y = 255
        self.options = {"grid_spacing": 50, "canW": 800, "canH": 600, "margin": 5}
        self.controller = controller
        Frame.__init__(self, master)
        self.grid()
        self.createSubFrames()

    def createSubFrames(self):
        """ Sets up the sub-frames: the canvas; the user input. """
        self.ViewsFrame = Frame(self,bd=5)
        self.ViewsFrame.grid(row=0, column=0)

        # the canvas
        width = self.options["canW"] + (1 * self.options["margin"])
        height = self.options["canH"] + (1 * self.options["margin"])
        options = {"width":width, "height":height, "bg":"black"}
        self.canvas = Canvas(self.ViewsFrame, options)
        self.canvas.grid(row=0, column=0)
        self.drawCanvasGrid()

        # the user input
        self.InputFrame = Frame(self,bd=5)
        self.InputFrame.grid(row=0, column=1)
        self.drawInputs()    


    def drawCanvasGrid(self):
        """ Provides the background grid for the canvas. """
        self.canvas.delete("grid")

        margin = self.options["margin"]
        width = self.options["canW"]
        height = self.options["canH"]
        grid_spacing = self.options["grid_spacing"]

        # vertical grid lines
        for i in xrange(0, int(width / grid_spacing)):
            self.canvas.create_line((i * grid_spacing) + margin + 50, margin,  (i * grid_spacing) + margin + 50, height + margin, fill="#888", tag="grid")
        # horizontal grid lines
        self.canvas.create_line(margin, self.scal_Y(0), width + margin, self.scal_Y(0), fill="#888", tag="grid")
        num_horizontal_lines = (int(height / grid_spacing) / 2) + 1
        for j in xrange(1, num_horizontal_lines):
            self.canvas.create_line(margin, self.scal_Y(0) + (j * grid_spacing), width + margin,  self.scal_Y(0) + (j * grid_spacing), fill="#888", tag="grid")
            self.canvas.create_line(margin, self.scal_Y(0) - (j * grid_spacing), width + margin,  self.scal_Y(0) - (j * grid_spacing), fill="#888", tag="grid")


    def gridAdjust(self, reference=1):
        """ This is to adjust the canvas grid to suit the chosen foil parameters. """
        grid_window = self.options["canW"] - 100    # magic number 100 is to get a 50 pixel margin
        # the magic number '10' determines how many units (mm now) per grid line
        new_grid_spacing = 10 * grid_window / reference
        if new_grid_spacing != self.options["grid_spacing"]:
            self.options["grid_spacing"] = new_grid_spacing
            self.drawCanvasGrid()


    def scal_X(self, num):
        return (num * self.scale) + self.translate_X


    def scal_Y(self, num):
        return (num * self.scale) + self.translate_Y


    def neg_scal_Y(self, num):
        return - (num * self.scale) + self.translate_Y



class FoilView(TabView):
    """ The FoilView Frame """
    def __init__(self, controller, master=None):
        TabView.__init__(self, controller, master)


    def drawInputs(self):
        """ Creates all of the user input elements appearing in the window. """

        # ****************************************************************************** #
        # ********************************** DRAW FOIL ********************************* #
        # ****************************************************************************** #
        row_num = 0
        self.section_width_label = Label(self.InputFrame, text='Section width - mm')
        self.section_width_label.grid(row=row_num, column=0)
        self.section_width_var = DoubleVar()
        self.section_width_input = Entry(self.InputFrame, textvariable=self.section_width_var ,width=15)
        self.section_width_input.grid(row=row_num, column=1)

        row_num += 1
        self.section_thickness_label = Label(self.InputFrame, text='Maximum thickness - mm')
        self.section_thickness_label.grid(row=row_num, column=0)
        self.section_thickness_var = DoubleVar()
        self.section_thickness_input = Entry(self.InputFrame, textvariable=self.section_thickness_var ,width=15)
        self.section_thickness_input.grid(row=row_num, column=1)

        # row_num += 1
        # self.laminate_thickness_label = Label(self.InputFrame, text='Laminate thickness (per side)')
        # self.laminate_thickness_label.grid(row=row_num, column=0)
        # self.laminate_thickness_var = DoubleVar()
        # self.laminate_thickness_input = Entry(self.InputFrame, textvariable=self.laminate_thickness_var ,width=15)
        # self.laminate_thickness_input.grid(row=row_num, column=1)

        row_num += 1
        self.regime_split_label = Label(self.InputFrame, text='Regime split point')
        self.regime_split_label.grid(row=row_num, column=0)
        self.regime_split_var = DoubleVar()
        self.regime_split_input = Scale(self.InputFrame, variable=self.regime_split_var, from_=0.8, to=1.0, orient=HORIZONTAL, resolution=0.01, length=150, sliderlength=20)
        self.regime_split_input.grid(row=row_num, column=1)

        row_num += 1
        self.radians_tolerance_label = Label(self.InputFrame, text='Facet tolerance - radians')
        self.radians_tolerance_label.grid(row=row_num, column=0)
        self.radians_tolerance_var = DoubleVar()
        self.radians_tolerance_input = Scale(self.InputFrame, variable=self.radians_tolerance_var, from_=.005, to=1.0, resolution=0.005, orient=HORIZONTAL,  length=150, sliderlength=20)
        self.radians_tolerance_input.grid(row=row_num, column=1)

        row_num += 1
        self.max_chine_length_label = Label(self.InputFrame, text='Maximum chine length - mm')
        self.max_chine_length_label.grid(row=row_num, column=0)
        self.max_chine_length_var = DoubleVar()
        self.max_chine_length_input = Scale(self.InputFrame, variable=self.max_chine_length_var, from_=.1, to=20.0, resolution=0.1, orient=HORIZONTAL,  length=150, sliderlength=20)
        self.max_chine_length_input.grid(row=row_num, column=1)

        row_num += 1
        self.button_drawfoil = Button(self.InputFrame,text="Generate foil",command=self.controller.generateFoil, width=30, bd=30)
        self.button_drawfoil.grid(row=row_num, column=0, columnspan=2, pady=5)

        row_num += 1
        ttk.Separator(self.InputFrame,orient=HORIZONTAL).grid(row=row_num, column=0, columnspan=2, sticky="ew", pady=5)

        # ****************************************************************************** #
        # ******************************* DRAW ROUGH CUTS ****************************** #
        # ****************************************************************************** #
        row_num += 1
        self.stock_width_label = Label(self.InputFrame, text='Stock width')
        self.stock_width_label.grid(row=row_num, column=0)
        self.stock_width_var = DoubleVar()
        self.stock_width_input = Entry(self.InputFrame, textvariable=self.stock_width_var ,width=15)
        self.stock_width_input.grid(row=row_num, column=1)

        row_num += 1
        self.stock_thickness_label = Label(self.InputFrame, text='Stock thickness')
        self.stock_thickness_label.grid(row=row_num, column=0)
        self.stock_thickness_var = DoubleVar()
        self.stock_thickness_input = Entry(self.InputFrame, textvariable=self.stock_thickness_var ,width=15)
        self.stock_thickness_input.grid(row=row_num, column=1)

        row_num += 1
        self.bit_diameter_label = Label(self.InputFrame, text='Cutter diameter - mm')
        self.bit_diameter_label.grid(row=row_num, column=0)
        self.bit_diameter_var = DoubleVar()
        self.bit_diameter_input = Spinbox(self.InputFrame, values=MC.bits, textvariable=self.bit_diameter_var, width=13)
        self.bit_diameter_input.grid(row=row_num, column=1)

        row_num += 1
        self.max_cut_area_label = Label(self.InputFrame, text='Cut area - mm^2')
        self.max_cut_area_label.grid(row=row_num, column=0)
        self.max_cut_area_var = DoubleVar()
        self.max_cut_area_input = Scale(self.InputFrame, variable=self.max_cut_area_var, from_=1.0, to=60.0, resolution=0.5, orient=HORIZONTAL,  length=150, sliderlength=20)
        self.max_cut_area_input.grid(row=row_num, column=1)

        row_num += 1
        self.button_roughcutcode = Button(self.InputFrame,text="Generate rough cuts and code",command=self.controller.saveGcode, width=30)
        self.button_roughcutcode.grid(row=row_num, column=0, columnspan=2, pady=5)

        row_num += 1
        ttk.Separator(self.InputFrame,orient=HORIZONTAL).grid(row=row_num, column=0, columnspan=2, sticky="ew", pady=5)


    def drawFoilChined(self, point_set):
        """ Used for drawing the cross-wise-cut foil, draws the foil profile
        with user-chosen parameters.
        Input: point_set is a list of tuples of (x,y) coordinates. """
        # TODO: draw a bunch of lines defined by the points in point_set
        pass

        # call self.gridAdjust(self.section_width_var.get())

    def drawRoughCut(self, point_set):
        """ This method runs in response to the "Generate rough cuts and code" button. """
        pass

        # call self.gridAdjust(self.section_width_var.get())

    def drawFoilPoints(self, point_set):
        """ This is the new way to draw the length-wise-cut foil. The full
        picture cannot be appreciated until drawRoughCut() is performed. """
        self.canvas.delete("profile")
        self.canvas.delete("ref_line")
        self.canvas.delete("tool_cut")
        self.gridAdjust()
        self.canvas.create_line(self.options["margin"], self.scal_Y(0), self.options["canW"], self.scal_Y(0), fill="green", tag="profile", dash=(5,10,40,10))

        # for (x,y) in point_set:


class StockView(TabView):
    def __init__(self, controller, master=None):
        TabView.__init__(self, controller, master)

    def drawInputs(self):
        pass
