from Tkinter import *
from math import *



class Application(Frame):
    def __init__(self, master=None):
        self.scale = 700
        self.translate_X = 55
        self.translate_Y = 255
        self.options = {"grid_spacing": 50, "canW": 800, "canH": 500, "margin": 5}
        Frame.__init__(self, master)
        self.grid()
        self.createWidgets()
        # self.drawFoil()


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
        self.num_points_label = Label(self.SubFrame, text='Number of profile points')
        self.num_points_label.grid(row=row_num, column=0)
        self.num_points_var = IntVar()
        self.num_points_input = Scale(self.SubFrame, variable=self.num_points_var, from_=31, to=1001, orient=HORIZONTAL,  length=150, sliderlength=20)
        self.num_points_input.grid(row=row_num, column=1)

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
        self.button_drawfoil = Button(self.SubFrame,text="Generate foil",command=self.drawFoilChined)
        self.button_drawfoil.grid(row=row_num, column=0, columnspan=2)


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
        bit_diam = 0.5 / foil_W
        bit_height = 0.75 / foil_W

        self.canvas.create_line(self.options["margin"], self.scal_Y(0), self.options["canW"], self.scal_Y(0), fill="green", tag="profile", dash=(5,10,40,10))

        prev_slope = pi / 2.0
        # note that x_prev is in domain [0,1.0]
        x_prev = 0
        y_prev = 0
        x_step = 0.05

        num_chines = 0

        if foil_W > 0 and foil_T > 0:
            t = foil_T / foil_W   # giving the NACA 00## number
            # for i in xrange(1, foil_points):
            #     x = i / (foil_points - 1.0)
            #     y = 5 * t * ((0.2969 * sqrt(x)) - (0.1260 * x) - (0.3516 * x**2) + (0.2843 * x**3) - (0.1015 * x**4))
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

                    # tool profile
                    if test_slope > 0:
                        self.canvas.create_rectangle(self.scal_X(x), self.neg_scal_Y(y), self.scal_X(x - bit_diam), self.neg_scal_Y(y + bit_height), tag="tool_cut")
                    elif test_slope * prev_slope < 0:
                        self.canvas.create_rectangle(self.scal_X(x_prev), self.neg_scal_Y(y_prev), self.scal_X(x_prev + bit_diam), self.neg_scal_Y(y_prev + bit_height), tag="tool_cut")
                        self.canvas.create_rectangle(self.scal_X(x), self.neg_scal_Y(y), self.scal_X(x + bit_diam), self.neg_scal_Y(y + bit_height), tag="tool_cut")
                    else:
                        self.canvas.create_rectangle(self.scal_X(x), self.neg_scal_Y(y), self.scal_X(x + bit_diam), self.neg_scal_Y(y + bit_height), tag="tool_cut")
                        pass
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
            self.canvas.itemconfig("tool_cut",  fill="#aa5555", outline="#883333")
            print num_chines


        # section of maximum thickness
        self.canvas.create_line(self.scal_X(0.3), self.options["canH"] / 4, self.scal_X(0.3), self.options["canH"] / 4 * 3 , tag="ref_line")

        # regime split section
        self.canvas.create_line(self.scal_X(foil_split), self.options["canH"] / 4, self.scal_X(foil_split), self.options["canH"] / 4 * 3 , tag="ref_line")
        self.canvas.itemconfig("ref_line", fill="cyan", dash=(30,8))

    def drawFoil(self):
        self.canvas.delete("profile")
        self.canvas.delete("ref_line")
        self.gridAdjust()

        # variables:
        #    - width
        #    - max thickness
        #    - laminate thickness (per side)
        #    - regime split point
        #    - number of points to break up the curve in facets
        foil_W = self.section_width_var.get()
        foil_T = self.section_thickness_var.get()
        lam_T = self.laminate_thickness_var.get()
        foil_split = self.regime_split_var.get()
        foil_points = self.num_points_var.get()
        if foil_points%2 == 0:
        	foil_points += 1

        self.canvas.create_line(self.options["margin"], self.scal_Y(0), self.options["canW"], self.scal_Y(0), fill="green", tag="profile", dash=(5,10,40,10))

        # note that x_prev is in domain [0,1.0]
        x_prev = 0
        y_prev = 0

        if foil_W > 0 and foil_T > 0:
            t = foil_T / foil_W   # giving the NACA 00## number
            for i in xrange(1, foil_points):
                x = i / (foil_points - 1.0)
                y = 5 * t * ((0.2969 * sqrt(x)) - (0.1260 * x) - (0.3516 * x**2) + (0.2843 * x**3) - (0.1015 * x**4))
                self.canvas.create_line(self.scal_X(x_prev), self.scal_Y(y_prev), self.scal_X(x), self.scal_Y(y), fill="yellow", tag="profile")
                self.canvas.create_line(self.scal_X(x_prev), self.neg_scal_Y(y_prev), self.scal_X(x), self.neg_scal_Y(y), fill="yellow", tag="profile")
                x_prev = x
                y_prev = y
                print x_prev

        # section of maximum thickness
        self.canvas.create_line(self.scal_X(0.3), self.options["canH"] / 4, self.scal_X(0.3), self.options["canH"] / 4 * 3 , tag="ref_line")

        # regime split section
        self.canvas.create_line(self.scal_X(foil_split), self.options["canH"] / 4, self.scal_X(foil_split), self.options["canH"] / 4 * 3 , tag="ref_line")
        self.canvas.itemconfig("ref_line", fill="cyan", dash=(30,10))


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

app = Application()
app.master.title("multi tinker")
app.mainloop()