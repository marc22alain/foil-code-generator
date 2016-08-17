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

        # must save the state of where the machine is in true space
        # start at machining blank's 0,0, which is -50mm from the first row of location holes
        # self.current_x = 0.0
        # self.current_y = 0.0
        self.safe_Z = 80.0
        self.pass_count = 0


    def setStock(self):
        pass
        # but, for example:
        # magic numbers from the designer's CAD system
        # foil_start is a ref from the blank's 0,0

        # test piece, section: 213 x 18.55, stock: 230 x 18.6:
        # self.foil_start, self.foil_length, self.skew_slope = (120.0, 80.0, 0.3)
        # self.centerline_Z = 18.6 / 2.0

        # BYTE blanks, section: 213 x 19.4, stock: 217 x 19.4:
        # self.foil_start, self.foil_length, self.skew_slope = (260.0, 460.0, 0.364)
        # self.centerline_Z = 19.4 / 2.0



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

