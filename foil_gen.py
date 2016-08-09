from Tkinter import *
import ttk
from math import *

import os
import sys


# START for local module imports:
path = os.getcwd().split("/")
# print path

new_path = ""
for i in xrange(1, len(path) - 1):
    new_path += "/" + path[i]
new_path += "/" + "G-code-repositories"
# print new_path

sys.path.append(new_path)

"""
FIXING unit confusion:

Units are used where:
    - user input (currently in inches)
    - drawing to the canvas (currently in range 0-1 over the section width)
    - MC_defaults (in metric, mm)
    - driving G-code generation (currently fucked-up)

"""

import Glib as G
import MC_defaults as MC
import simple_generators as SG
# END for local module imports:


class Application(Frame):
    def __init__(self, master=None):
        self.scale = 700
        self.translate_X = 55
        self.translate_Y = 255
        self.options = {"grid_spacing": 50, "canW": 800, "canH": 600, "margin": 5}
        self.gcode_generator = GCodeGenerator()
        self.gcode_stage = ""
        Frame.__init__(self, master)
        self.grid()
        self.createWidgets()


    def createWidgets(self):

        self.EntryFrame = Frame(self,bd=5)
        self.EntryFrame.grid(row=0, column=0)

        # the canvas
        width = self.options["canW"] + (1 * self.options["margin"])
        height = self.options["canH"] + (1 * self.options["margin"])
        options = {"width":width, "height":height, "bg":"black"}
        self.canvas = Canvas(self.EntryFrame, options)
        self.canvas.grid(row=0, column=0)
        self.drawCanvasGrid()

        # the user input
        self.SubFrame = Frame(self,bd=5)
        self.SubFrame.grid(row=0, column=1)
        self.drawButtons()    


    def drawCanvasGrid(self):
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


    def drawButtons(self):

        # ****************************************************************************** #
        # ********************************** DRAW FOIL ********************************* #
        # ****************************************************************************** #
        row_num = 0
        self.section_width_label = Label(self.SubFrame, text='Section width - mm')
        self.section_width_label.grid(row=row_num, column=0)
        self.section_width_var = DoubleVar()
        self.section_width_input = Entry(self.SubFrame, textvariable=self.section_width_var ,width=15)
        self.section_width_input.grid(row=row_num, column=1)

        row_num += 1
        self.section_thickness_label = Label(self.SubFrame, text='Maximum thickness - mm')
        self.section_thickness_label.grid(row=row_num, column=0)
        self.section_thickness_var = DoubleVar()
        self.section_thickness_input = Entry(self.SubFrame, textvariable=self.section_thickness_var ,width=15)
        self.section_thickness_input.grid(row=row_num, column=1)

        row_num += 1
        self.laminate_thickness_label = Label(self.SubFrame, text='Laminate thickness (per side)')
        self.laminate_thickness_label.grid(row=row_num, column=0)
        self.laminate_thickness_var = DoubleVar()
        self.laminate_thickness_input = Entry(self.SubFrame, textvariable=self.laminate_thickness_var ,width=15)
        self.laminate_thickness_input.grid(row=row_num, column=1)

        row_num += 1
        self.regime_split_label = Label(self.SubFrame, text='Regime split point')
        self.regime_split_label.grid(row=row_num, column=0)
        self.regime_split_var = DoubleVar()
        self.regime_split_input = Scale(self.SubFrame, variable=self.regime_split_var, from_=0.8, to=1.0, orient=HORIZONTAL, resolution=0.01, length=150, sliderlength=20)
        self.regime_split_input.grid(row=row_num, column=1)

        row_num += 1
        self.facet_tolerance_label = Label(self.SubFrame, text='Facet tolerance - radians')
        self.facet_tolerance_label.grid(row=row_num, column=0)
        self.facet_tolerance_var = DoubleVar()
        self.facet_tolerance_input = Scale(self.SubFrame, variable=self.facet_tolerance_var, from_=.005, to=1.0, resolution=0.005, orient=HORIZONTAL,  length=150, sliderlength=20)
        self.facet_tolerance_input.grid(row=row_num, column=1)

        row_num += 1
        self.max_chine_length_label = Label(self.SubFrame, text='Maximum chine length - mm')
        self.max_chine_length_label.grid(row=row_num, column=0)
        self.max_chine_length_var = DoubleVar()
        self.max_chine_length_input = Scale(self.SubFrame, variable=self.max_chine_length_var, from_=.1, to=20.0, resolution=0.1, orient=HORIZONTAL,  length=150, sliderlength=20)
        self.max_chine_length_input.grid(row=row_num, column=1)

        row_num += 1
        self.button_drawfoil = Button(self.SubFrame,text="Generate foil",command=self.drawFoilChined, width=30, bd=30)
        self.button_drawfoil.grid(row=row_num, column=0, columnspan=2, pady=5)

        row_num += 1
        ttk.Separator(self.SubFrame,orient=HORIZONTAL).grid(row=row_num, column=0, columnspan=2, sticky="ew", pady=5)

        # ****************************************************************************** #
        # ******************************* DRAW ROUGH CUTS ****************************** #
        # ****************************************************************************** #
        row_num += 1
        self.stock_width_label = Label(self.SubFrame, text='Stock width')
        self.stock_width_label.grid(row=row_num, column=0)
        self.stock_width_var = DoubleVar()
        self.stock_width_input = Entry(self.SubFrame, textvariable=self.stock_width_var ,width=15)
        self.stock_width_input.grid(row=row_num, column=1)

        row_num += 1
        self.stock_thickness_label = Label(self.SubFrame, text='Stock thickness')
        self.stock_thickness_label.grid(row=row_num, column=0)
        self.stock_thickness_var = DoubleVar()
        self.stock_thickness_input = Entry(self.SubFrame, textvariable=self.stock_thickness_var ,width=15)
        self.stock_thickness_input.grid(row=row_num, column=1)

        row_num += 1
        self.bit_diameter_label = Label(self.SubFrame, text='Cutter diameter - mm')
        self.bit_diameter_label.grid(row=row_num, column=0)
        self.bit_diameter_var = DoubleVar()
        self.bit_diameter_input = Spinbox(self.SubFrame, values=MC.bits, textvariable=self.bit_diameter_var, width=13)
        self.bit_diameter_input.grid(row=row_num, column=1)

        row_num += 1
        self.max_cut_area_label = Label(self.SubFrame, text='Cut area - mm^2')
        self.max_cut_area_label.grid(row=row_num, column=0)
        self.max_cut_area_var = DoubleVar()
        self.max_cut_area_input = Scale(self.SubFrame, variable=self.max_cut_area_var, from_=1.0, to=60.0, resolution=0.5, orient=HORIZONTAL,  length=150, sliderlength=20)
        self.max_cut_area_input.grid(row=row_num, column=1)

        row_num += 1
        self.button_roughcutcode = Button(self.SubFrame,text="Generate rough cuts and code",command=self.drawRoughCut, width=30)
        self.button_roughcutcode.grid(row=row_num, column=0, columnspan=2, pady=5)

        row_num += 1
        ttk.Separator(self.SubFrame,orient=HORIZONTAL).grid(row=row_num, column=0, columnspan=2, sticky="ew", pady=5)

        # ****************************************************************************** #
        # ******************************** MAKE FINE CUTS ****************************** #
        # ****************************************************************************** #
        row_num += 1
        self.ball_nose_diameter_label = Label(self.SubFrame, text='Ball nose diameter - mm')
        self.ball_nose_diameter_label.grid(row=row_num, column=0)
        self.ball_nose_diameter_var = DoubleVar()
        self.ball_nose_diameter_input = Spinbox(self.SubFrame, values=MC.ball_noses, textvariable=self.ball_nose_diameter_var, width=13, command=self.updatePassSlider)
        self.ball_nose_diameter_input.grid(row=row_num, column=1)

        row_num += 1
        self.pass_spacing_label = Label(self.SubFrame, text='Pass spacing - mm')
        self.pass_spacing_label.grid(row=row_num, column=0)
        self.pass_spacing_var = DoubleVar()
        self.pass_spacing_input = Scale(self.SubFrame, variable=self.pass_spacing_var, from_=0.0, to=self.ball_nose_diameter_var.get(), resolution=0.5, orient=HORIZONTAL,  length=150, sliderlength=20)
        self.pass_spacing_input.grid(row=row_num, column=1)

        row_num += 1
        self.button_finecutcode = Button(self.SubFrame,text="Generate fine cuts and code",command=self.genFineCut, width=30)
        self.button_finecutcode.grid(row=row_num, column=0, columnspan=2, pady=5)

        row_num += 1
        ttk.Separator(self.SubFrame,orient=HORIZONTAL).grid(row=row_num, column=0, columnspan=2, sticky="ew", pady=5)

        # ****************************************************************************** #
        # ********************************** SAVE FILE ********************************* #
        # ****************************************************************************** #
        row_num += 1
        self.file_name_label = Label(self.SubFrame, text='File name')
        self.file_name_label.grid(row=row_num, column=0)
        self.file_name_var = StringVar()
        self.file_name_input = Entry(self.SubFrame, textvariable=self.file_name_var ,width=15)
        self.file_name_input.grid(row=row_num, column=1)

        row_num += 1
        self.button_save_gcode_code = Button(self.SubFrame,text="Save g-code",command=self.saveGcode, width=30)
        self.button_save_gcode_code.grid(row=row_num, column=0, columnspan=2, pady=5)

        row_num += 1
        ttk.Separator(self.SubFrame,orient=HORIZONTAL).grid(row=row_num, column=0, columnspan=2, sticky="ew", pady=5)


    def updatePassSlider(self):
        print "called updatePassSlider"
        print self.ball_nose_diameter_var.get()
        print self.pass_spacing_input.config({"to":self.ball_nose_diameter_var.get()})


    def drawFoilChined(self):
        """ AKA the 'Generate foil' button. """
        self.canvas.delete("profile")
        self.canvas.delete("ref_line")
        self.canvas.delete("tool_cut")
        self.gridAdjust()
        # variables:
        #    - width
        #    - max thickness
        #    - laminate thickness (per side)
        #    - regime split point
        foil_W = self.section_width_var.get()
        foil_T = self.section_thickness_var.get()
        lam_T = self.laminate_thickness_var.get()
        foil_split = self.regime_split_var.get()
        foil_facet_tol = self.facet_tolerance_var.get()
        max_chine_length = self.max_chine_length_var.get() / foil_W

        self.canvas.create_line(self.options["margin"], self.scal_Y(0), self.options["canW"], self.scal_Y(0), fill="green", tag="profile", dash=(5,10,40,10))

        prev_slope = pi / 2.0
        # note that x_prev is in domain [0,1.0]
        x_prev = 0
        y_prev = 0
        x_step = 0.05

        self.point_set = [(x_prev, y_prev, prev_slope)]

        num_chines = 0

        if foil_W > 0 and foil_T > 0:
            t = foil_T / foil_W   # giving the NACA 00## number

            while (x_prev < 1.0):
                assert x_step <= 0.3
                x = x_prev + x_step
                if x > 1.0:
                    x = 1.0
                y = 5 * t * ((0.2969 * sqrt(x)) - (0.1260 * x) - (0.3516 * x**2) + (0.2843 * x**3) - (0.1015 * x**4))
                test_slope = atan((y - y_prev) / (x - x_prev))

                if (abs(abs(test_slope - prev_slope) - foil_facet_tol) < foil_facet_tol / 10) or (x_step == max_chine_length):
                    num_chines += 1
                    # chine lines
                    self.canvas.create_line(self.scal_X(x_prev), self.scal_Y(y_prev), self.scal_X(x), self.scal_Y(y), fill="yellow", tag="profile")
                    self.canvas.create_line(self.scal_X(x_prev), self.neg_scal_Y(y_prev), self.scal_X(x), self.neg_scal_Y(y), fill="yellow", tag="profile")

                    # tick marks
                    self.canvas.create_line(self.scal_X(x), self.neg_scal_Y(y), self.scal_X(x), self.neg_scal_Y(y) + 10, fill="magenta", tag="profile")

                    self.point_set.append((x, y, test_slope))
                    x_prev = x
                    y_prev = y
                    prev_slope = test_slope
                    x_step = 0.05

                else:
                    if prev_slope - test_slope - foil_facet_tol > 0:
                        x_step /= 2.0
                    else:
                        x_step *= 1.5
                        if x_step > max_chine_length:
                            x_step = max_chine_length

            print num_chines


        # section of maximum thickness
        self.canvas.create_line(self.scal_X(0.3), self.options["canH"] / 4, self.scal_X(0.3), self.options["canH"] / 4 * 3 , tag="ref_line")

        # regime split section
        self.canvas.create_line(self.scal_X(foil_split), self.options["canH"] / 4, self.scal_X(foil_split), self.options["canH"] / 4 * 3 , tag="ref_line")
        self.canvas.itemconfig("ref_line", fill="cyan", dash=(30,8))
        # truncation width calculation
        self.showFoilTruncation()

        return num_chines


    def drawRoughCut(self):
        """
        This method runs in response to the "Generate rough cuts and code" button.
        It must first wipe the slate clean before making new gcode.
        """
        self.gcode_generator.wipeClean()
        # note that no unit conversions are required here, as the input is in the user units
        self.gcode_generator.startProgram(self.section_width_var.get(), self.stock_width_var.get(), self.stock_thickness_var.get())

        self.canvas.delete("tool_cut")
        self.canvas.delete("stock")

        self.stock_width = self.stock_width_var.get()
        self.stock_thickness = self.stock_thickness_var.get()
        assert self.stock_width != 0 and self.stock_thickness != 0, "rough stock is not sufficiently defined"
        assert len(self.point_set) > 1, "you must define a foil first"

        foil_W = self.section_width_var.get()
        foil_T = self.section_thickness_var.get() / foil_W
        # Converts metric to the plot's single unit unit
        bit_diam = self.bit_diameter_var.get() / foil_W
        # Another magic number, until MC_defaults contains all required info
        # TODO: update MC_defaults for more bit information
        bit_height = 20.0 / foil_W

        over_W = (self.stock_width - foil_W) / 2.0 / foil_W
        # original definition, coincident centerline of foil with centerline of blank
        # over_T = (self.stock_thickness ) / 2.0 / foil_W
        over_T = (self.stock_thickness / foil_W) - (foil_T / 2.0)

        x_prev = - over_W
        y_prev = 0
        prev_slope = pi / 2.0  # don't remember ? why not pi / 2

        # stock
        self.canvas.create_rectangle(self.scal_X( - over_W), self.neg_scal_Y(over_T), self.scal_X( 1 + over_W), self.scal_Y(foil_T / 2.0),  fill="", outline="white", tag="stock")

        # tool profile
        for i in xrange(0, len(self.point_set)):
            x = self.point_set[i][0]
            y = self.point_set[i][1]
            test_slope = self.point_set[i][2]

            if test_slope > 0:
                # self.canvas.create_rectangle(self.scal_X(x), self.neg_scal_Y(y), self.scal_X(x - bit_diam), self.neg_scal_Y(min(over_T, y + bit_height)), tag="tool_cut")
                self._drawRoughCut(x, y, x - bit_diam, min(over_T, y + bit_height), x_prev)
                # pass
            elif test_slope * prev_slope < 0:
                # self.canvas.create_rectangle(self.scal_X(x_prev), self.neg_scal_Y(y_prev), self.scal_X(x_prev + bit_diam), self.neg_scal_Y(min(over_T, y + bit_height)), tag="tool_cut")
                self._drawRoughCut(x, y, x - bit_diam, min(over_T, y + bit_height), x_prev)
                # self.canvas.create_rectangle(self.scal_X(x), self.neg_scal_Y(y), self.scal_X(x + bit_diam), self.neg_scal_Y(min(over_T, y + bit_height)), tag="tool_cut")
                self._drawRoughCut(x + bit_diam, y, x, min(over_T, y + bit_height), x)
                # pass
            else:
                # self.canvas.create_rectangle(self.scal_X(x), self.neg_scal_Y(y), self.scal_X(x + bit_diam), self.neg_scal_Y(min(over_T, y + bit_height)), tag="tool_cut")
                self._drawRoughCut(x + bit_diam, y, x, min(over_T, y + bit_height), x_prev + bit_diam)
                # pass
            x_prev = x
            y_prev = y
            prev_slope = test_slope

        self.canvas.itemconfig("tool_cut",  fill="#aa5555", outline="#883333")

        self.gcode_generator.endProgram()

        self.gcode_stage = "rough"

        print "Number of passes is %s" % self.gcode_generator.pass_count


    def _drawRoughCut(self, x_right, y_bottom, x_left, y_top, x_prev):
        """
        Input arguments define the actual area to be cut in this pass.
        Each call defines a new pass; should trigger a shift to the new X (or Y depending on stock layout in the machine) coordinate.
        Each pass of the while loop should trigger a new depth of cut, i.e. a new shift in Z, and a new pass across the stock.
        NOTE: an odd number of passes will leave the bit at the opposite end of the stock.
        """
        # need this to convert units back to input metric
        foil_W = self.section_width_var.get()
        # first make the gcode move to new pass X location... defined by the bit's center
        # ... and convert from single unit units back to metric mm
        self.gcode_generator.shiftX( foil_W * (x_right + x_left) / 2.0 )

        max_cut_area = self.max_cut_area_var.get() / self.section_width_var.get()**2

        # total_cut_area takes into account the overlap, but misses the increased width of cut when increasing the depth of cut
        total_cut_area = (y_top - y_bottom) * ( x_right - x_prev)
        assert total_cut_area > 0, "total_cut_area %f, y_top %f, y_bottom %f, x_right %f, x_prev %f" % \
                                    (total_cut_area, y_top, y_bottom, x_right, x_prev)
        y_left = y_top - y_bottom
        y_incr = min(max_cut_area / total_cut_area, 1) * y_left
        y_prev_dest = y_top
        while y_left > 0:
            y_dest = max(y_bottom, y_prev_dest - y_incr)
            # now make the gcode for the pass across the stock
            # ...and convert from the single unit units back to metric input mm 
            self.gcode_generator.shiftY( y_dest * foil_W)
            # now draw this pass
            self.canvas.create_rectangle(self.scal_X(x_right), self.neg_scal_Y(y_dest), self.scal_X(x_left), self.neg_scal_Y(y_prev_dest), tag="tool_cut")
            y_prev_dest = y_dest
            y_left -= y_incr


    def genFineCut(self):
        """
        Input required:
            - ball-nose bit selection (from defaults)
            - pass-spacing
        Output required:
            - user feedback telling that operation was performed
            - calculate peak between passes ?
            - lay computed arcs over fine-drawn foil
        """
        foil_W = self.section_width_var.get()
        saved_foil_facet_tol = self.facet_tolerance_var.get()
        saved_max_chine_length = self.max_chine_length_var.get()
        # note that 0.005 radians is 0.286 degrees
        self.facet_tolerance_var.set(0.005)
        self.max_chine_length_var.set(0.1)
        self.drawFoilChined()

        self.facet_tolerance_var.set(saved_foil_facet_tol)
        self.max_chine_length_var.set(saved_max_chine_length)

        # self.point_set is renewed !
        """
        Algorithm is:
            - making two sets of instructions: one each way across the foil section
            - get the ball-nose cutter to start at the leading edge, corner point tangent to centerline
            - make a G2 in YZ (or XZ) plane to put a the bit tangent to the next line in the series
            - make a G1 in YZ (or XZ) plane to put the the new tangent point at the end of the line
            - repeat until reached the end of the foil
            - make a G1 move in X (or Y) to ready for the pass back over the foil section 
            - repeat the foil section machining in a backwards manner
        """
        # make first pass
        # G0_XY to outside of stock edge
        # G0_Z so that vertical tangent point of ball-nose is at the horizontal centerline of the stock
        # G1_XY to put cutter at the start of the foil leading edge
        # ... then enter the foor loop
        # note that if the centerline start point is at (0, 0.5) and the ball-nose R = 0.25, then the machine is at (-0.25, 0.25)
        for i in xrange(len(self.point_set)):
            # REM: that point_set[0] is the origin with slope of pi / 2
            # G2 in blah-blah plane, with the i-th point set coords as the center point
            #   - how is the end-point defined ?
            # an incremental G2 approach would be to define the center_point as (cos(prev_slope - (pi/2)), sin(prev_slope - (pi/2))) * bit_radius
            #   - and end-point as center_point - (cos(new_slope - (pi/2)), sin(new_slope - (pi/2))) * bit_radius)
            pass


    def saveGcode(self):
        user_name = self.file_name_var.get()

        foil_aspect = str(int( 100 * self.section_thickness_var.get() / self.section_width_var.get() ))
        default_name =  "00" + foil_aspect + "_" + self.gcode_stage

        if user_name == "":
            file_name = default_name + ".ngc"
            file_name_mirror = default_name + "_mirror.ngc"
        else:
            file_name = user_name + ".ngc"
            file_name_mirror = user_name + "_mirror.ngc"

        gcode, gcode_mirror = self.gcode_generator.getGCode()
        print gcode
        print
        print "This g-code saved in file with name:", file_name

        with open(file_name, 'w') as myFile:
            myFile.write(gcode)

        with open(file_name_mirror, 'w') as myFile:
            myFile.write(gcode_mirror)


    def gridAdjust(self):
    	grid_window = self.options["canW"] - 100    # magic number 100 is to get a 50 pixel margin
        foil_W = self.section_width_var.get()
        # the magic number '10' determines how many units (mm now) per grid line
        new_grid_spacing = 10 * grid_window / foil_W
        if new_grid_spacing != self.options["grid_spacing"]:
        	self.options["grid_spacing"] = new_grid_spacing
        	self.drawCanvasGrid()


    def scal_X(self, num):
        return (num * self.scale) + self.translate_X


    def scal_Y(self, num):
        return (num * self.scale) + self.translate_Y


    def neg_scal_Y(self, num):
        return - (num * self.scale) + self.translate_Y

    def showFoilTruncation(self):
        foil_split = self.regime_split_var.get()
        foil_W = self.section_width_var.get()
        foil_T = self.section_thickness_var.get()
        t = foil_T / foil_W   # giving the NACA 00## number
        x = 1 * foil_split
        y = 5 * t * ((0.2969 * sqrt(x)) - (0.1260 * x) - (0.3516 * x**2) + (0.2843 * x**3) - (0.1015 * x**4))
        print "foil truncation width is %s" % (2 * y * foil_W)


class GCodeGenerator(object):
    """
    Coordinate mapping between wizard UI's plot and the CNC machine:
    - X of plot is Y of machine
    - Y of plot is Z of machine
    - no representation of machine's X
    """
    def __init__(self):
        self.gcode = self.gcode_mirror = ""
        # sentinel variable indicating which end of the foil the machine is currently at
        self.router_at_foil_start = True
        # magic numbers from the designer's CAD system
        # foil_start is a ref from the blank's 0,0

        # test piece, section: 213 x 18.55, stock: 230 x 18.6:
        # self.foil_start, self.foil_length, self.skew_slope = (120.0, 80.0, 0.3)
        # self.centerline_Z = 18.6 / 2.0

        # BYTE blanks, section: 213 x 19.4, stock: 217 x 19.4:
        self.foil_start, self.foil_length, self.skew_slope = (260.0, 460.0, 0.364)
        self.centerline_Z = 19.4 / 2.0

        # must save the state of where the machine is in true space
        # start at machining blank's 0,0, which is -50mm from the first row of location holes
        # self.current_x = 0.0
        # self.current_y = 0.0
        self.safe_Z = 80.0
        self.pass_count = 0


    def wipeClean(self):
        self.gcode = self.gcode_mirror = ""
        self.router_at_foil_start = True
        self.pass_count = 0


    def startProgram(self, section_width, stock_width, stock_thickness):
        self.gcode += SG.startProgram(MC.default_feed_rate)
        self.gcode_mirror += SG.startProgram(MC.default_feed_rate)

        self.gcode += G.set_ABS_mode()
        self.gcode_mirror += G.set_ABS_mode()

        self.section_width = section_width
        self.stock_width = stock_width
        self.foil_stock_offset = (self.stock_width - self.section_width) / 2.0
        self.above_stock = stock_thickness + 1.0
        # assumes only protrusions above the stock are the bolt heads at location rows
        self.safe_Z = stock_thickness + 10.0

        self.gcode += G.G0_Z(self.safe_Z)
        self.gcode_mirror += G.G0_Z(self.safe_Z)

        # sets the machine at the starting point of the foil's leading edge
        self.gcode += G.G0_XY((self.foil_start, self.foil_stock_offset))
        self.gcode_mirror += G.G0_XY((self.foil_start, self.stock_width - self.foil_stock_offset))


    def getGCode(self):
        return self.gcode, self.gcode_mirror


    def shiftX(self, new_x):
        """
        X refers to the plot X axis. Current assumption is that this will be a G0 in machine's Y.
        new_x is an absolute coordinate.

        This method implements the skew.
        """
        # move in machine Z to just above the stock
        self.gcode += G.G0_Z(self.above_stock)
        self.gcode_mirror += G.G0_Z(self.above_stock)
        # move to new X; this is in the machine's Y axis

        # original
        # self.gcode += G.G0_Y(new_x)

        # new for skewed foils
        if self.router_at_foil_start == True:
            self.gcode += G.G0_XY( (self.foil_start + (new_x * self.skew_slope), new_x + self.foil_stock_offset) )
            self.gcode_mirror += G.G0_XY( (self.foil_start + (new_x * self.skew_slope), self.stock_width - (new_x + self.foil_stock_offset) ) )
        else:
            self.gcode += G.G0_XY( (self.foil_start + (new_x * self.skew_slope) + self.foil_length, new_x + self.foil_stock_offset) )
            self.gcode_mirror += G.G0_XY( (self.foil_start + (new_x * self.skew_slope) + self.foil_length, self.stock_width - (new_x + self.foil_stock_offset) ) )


    def shiftY(self, new_y):
        """
        Y refers to the plot Y axis.
        new_y is an absolute coordinate.
        """
        # move to new machine Z with G1
        self.gcode += G.G1_Z(new_y + self.centerline_Z)
        self.gcode_mirror += G.G1_Z(new_y + self.centerline_Z)
        # make a cutting pass across the stock; this is in the machine's X axis

        # original
        # if self.router_at_foil_start == True:
        #     self.gcode += G.G1_X(self.foil_end)
        # else:
        #     self.gcode += G.G1_X(0)

        # new
        self.gcode += G.set_INCR_mode()
        self.gcode_mirror += G.set_INCR_mode()

        if self.router_at_foil_start == True:
            self.gcode += G.G1_X(self.foil_length)
            self.gcode_mirror += G.G1_X(self.foil_length)

        else:
            self.gcode += G.G1_X(- self.foil_length)
            self.gcode_mirror += G.G1_X(- self.foil_length)

        self.gcode += G.set_ABS_mode()
        self.gcode_mirror += G.set_ABS_mode()
        # flip the foil end sentinel
        self.router_at_foil_start = not self.router_at_foil_start
        # count this pass
        self.pass_count += 1


    def endProgram(self):
        self.gcode += G.G0_Z(self.safe_Z)
        self.gcode_mirror += G.G0_Z(self.safe_Z)

        self.gcode += G.G0_XY((0,0))
        self.gcode_mirror += G.G0_XY((0,0))

        self.gcode += SG.endProgram()
        self.gcode_mirror += SG.endProgram()



app = Application()
app.master.title("Foil Generator")
app.mainloop()