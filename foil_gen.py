from Tkinter import *
import ttk
from math import *
import MC_defaults as MC
import simple_generators as SG
import Glib as G



class Application(Frame):
    def __init__(self, master=None):
        self.scale = 700
        self.translate_X = 55
        self.translate_Y = 255
        self.options = {"grid_spacing": 50, "canW": 800, "canH": 500, "margin": 5}
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

        row_num = 0
        self.section_width_label = Label(self.SubFrame, text='Section width')
        self.section_width_label.grid(row=row_num, column=0)
        self.section_width_var = DoubleVar()
        self.section_width_input = Entry(self.SubFrame, textvariable=self.section_width_var ,width=15)
        self.section_width_input.grid(row=row_num, column=1)

        row_num += 1
        self.section_thickness_label = Label(self.SubFrame, text='Maximum thickness')
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
        self.max_chine_length_label = Label(self.SubFrame, text='Maximum chine length - inches')
        self.max_chine_length_label.grid(row=row_num, column=0)
        self.max_chine_length_var = DoubleVar()
        self.max_chine_length_input = Scale(self.SubFrame, variable=self.max_chine_length_var, from_=.125, to=0.500, resolution=0.025, orient=HORIZONTAL,  length=150, sliderlength=20)
        self.max_chine_length_input.grid(row=row_num, column=1)

        row_num += 1
        self.button_drawfoil = Button(self.SubFrame,text="Generate foil",command=self.drawFoilChined, width=30, bd=30)
        self.button_drawfoil.grid(row=row_num, column=0, columnspan=2, pady=5)

        row_num += 1
        ttk.Separator(self.SubFrame,orient=HORIZONTAL).grid(row=row_num, column=0, columnspan=2, sticky="ew", pady=5)

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
        self.max_cut_area_input = Scale(self.SubFrame, variable=self.max_cut_area_var, from_=1.0, to=15.0, resolution=0.5, orient=HORIZONTAL,  length=150, sliderlength=20)
        self.max_cut_area_input.grid(row=row_num, column=1)

        row_num += 1
        self.button_roughcutcode = Button(self.SubFrame,text="Generate rough cuts and code",command=self.drawRoughCut, width=30)
        self.button_roughcutcode.grid(row=row_num, column=0, columnspan=2, pady=5)

        row_num += 1
        ttk.Separator(self.SubFrame,orient=HORIZONTAL).grid(row=row_num, column=0, columnspan=2, sticky="ew", pady=5)

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

    def drawFoilChined(self):
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


    def drawRoughCut(self):
        """
        This method runs in response to the "Generate rough cuts and code" button.
        It must first wipe the slate clean before making new gcode.
        """
        self.gcode_generator.wipeClean()
        self.gcode_generator.startProgram()
        self.gcode_generator.setStockThickness(self.stock_thickness_var.get())

        self.canvas.delete("tool_cut")
        self.canvas.delete("stock")

        self.stock_width = self.stock_width_var.get()
        self.stock_thickness = self.stock_thickness_var.get()
        assert self.stock_width != 0 and self.stock_thickness != 0, "rough stock is not sufficiently defined"
        assert len(self.point_set) > 1, "you must define a foil first"

        foil_W = self.section_width_var.get()
        foil_T = self.section_thickness_var.get() / foil_W
        bit_diam = self.bit_diameter_var.get() / 25.4 / foil_W
        bit_height = 0.75 / foil_W

        over_W = (self.stock_width - foil_W) / 2.0 / foil_W
        over_T = (self.stock_thickness ) / 2.0 / foil_W

        x_prev = - over_W
        y_prev = 0
        prev_slope = 1

        # stock
        self.canvas.create_rectangle(self.scal_X( - over_W), self.neg_scal_Y(over_T), self.scal_X( 1 + over_W), self.scal_Y(over_T),  fill="", outline="white", tag="stock")

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


    def _drawRoughCut(self, x_right, y_bottom, x_left, y_top, x_prev):
        """
        Input arguments define the actual area to be cut in this pass.
        Each call defines a new pass; should trigger a shift to the new X (or Y depending on stock layout in the machine) coordinate.
        Each pass of the while loop should trigger a new depth of cut, i.e. a new shift in Z, and a new pass across the stock.
        NOTE: an odd number of passes will leave the bit at the opposite end of the stock.
        """
        # first make the gcode move to new pass X location... defined by the bit's center.
        self.gcode_generator.shiftX( (x_right + x_left) / 2.0 )

        max_cut_area = self.max_cut_area_var.get() / 25.4**2 / self.section_width_var.get()**2
        total_cut_area = (y_top - y_bottom) * ( min( x_right, self.stock_width_var.get() / self.section_width_var.get() ) - x_prev)
        assert total_cut_area > 0, "y_top %f, y_bottom %f, x_right %f, x_prev %f" % (y_top, y_bottom, x_right, x_prev)
        y_left = y_top - y_bottom
        y_incr = min(max_cut_area / total_cut_area, 1) * y_left
        y_prev_dest = y_top
        while y_left > 0:
            y_dest = max(y_bottom, y_prev_dest - y_incr)
            # now make the gcode for the pass across the stock
            self.gcode_generator.shiftY( y_dest )
            # now draw this pass
            self.canvas.create_rectangle(self.scal_X(x_right), self.neg_scal_Y(y_dest), self.scal_X(x_left), self.neg_scal_Y(y_prev_dest), tag="tool_cut")
            y_prev_dest = y_dest
            y_left -= y_incr


    def saveGcode(self):
        user_name = self.file_name_var.get()

        foil_aspect = str(int( 100 * self.section_thickness_var.get() / self.section_width_var.get() ))
        default_name =  "00" + foil_aspect + "_" + self.gcode_stage

        if user_name == "":
            file_name = default_name + ".ngc"
        else:
            file_name = user_name + ".ngc"

        print self.gcode_generator.getGCode()
        print
        print "This g-code saved in file with name:", file_name

        with open(file_name, 'w') as myFile:
            myFile.write(self.gcode_generator.getGCode())


    def gridAdjust(self):
    	grid_window = self.options["canW"] - 100    # magic number 100 is to get a 50 pixel margin
        foil_W = self.section_width_var.get()
        new_grid_spacing = grid_window / foil_W
        if new_grid_spacing != self.options["grid_spacing"]:
        	self.options["grid_spacing"] = new_grid_spacing
        	self.drawCanvasGrid()


    def scal_X(self, num):
        return (num * self.scale) + self.translate_X


    def scal_Y(self, num):
        return (num * self.scale) + self.translate_Y


    def neg_scal_Y(self, num):
        return - (num * self.scale) + self.translate_Y



class GCodeGenerator(object):
    def __init__(self):
        self.gcode = ""
        self.router_at_stock_start = True
        self.stock_end = 100


    def wipeClean(self):
        self.gcode = ""
        self.router_at_stock_start = True


    def startProgram(self):
        self.gcode += SG.startProgram(MC.default_feed_rate)
        self.gcode += G.set_ABS_mode()

    def setStockThickness(self, stock_thickness):
        # More on the unit inconsistencies: must translate plot's inches to machine's metric
        self.above_stock = stock_thickness * 25.4


    def getGCode(self):
        return self.gcode


    def shiftX(self, new_x):
        """
        X refers to the plot X axis. Current assumption is that this will be a G0 in machine's Y.
        new_x is an absolute coordinate.
        """
        # move in machine Z to just above the stock
        self.gcode += G.G0_Z(self.above_stock)
        # move to new X (or Y depending on stock layout in the machine)
        self.gcode += G.G0_Y(new_x * 25.4)


    def shiftY(self, new_y):
        """
        X refers to the plot X axis.
        new_x is an absolute coordinate.
        """
        # move to new machine Z with G1
        self.gcode += G.G1_Z(new_y * 25.4)
        # make a cutting pass across the stock, assuming that this is in the machine's X axis
        if self.router_at_stock_start == True:
            self.gcode += G.G1_X(self.stock_end)
        else:
            self.gcode += G.G1_X(0)
        # flip the stock end sentinel
        self.router_at_stock_start = not self.router_at_stock_start

    def endProgram(self):
        self.gcode += SG.endProgram()



app = Application()
app.master.title("Foil Generator")
app.mainloop()