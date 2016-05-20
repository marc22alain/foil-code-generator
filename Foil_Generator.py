from Tkinter import *
from GeoCanvas import GeoFrame



class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.grid()
        self.createSubFrames()


    def createSubFrames(self):
    	self.FoilGeoCanvas = FoilCanvas(self)

    	self.FoilEntryFrame = FoilEntry(self)

        # self.EntryFrame = Frame(self,bd=5)
        # self.EntryFrame.grid(row=0, column=1)

    #     # the canvas
    #     width = self.options["canW"] + (1 * self.options["margin"])
    #     height = self.options["canH"] + (1 * self.options["margin"])
    #     options = {"width":width, "height":height, "bg":"black"}
    #     self.canvas = Canvas(self.EntryFrame, options)
    #     self.canvas.grid(row=0, column=0)
    #     self.drawCanvasGrid()


    #     self.SubFrame = Frame(self,bd=5)
    #     self.SubFrame.grid(row=0, column=1)

    #     self.drawButtons()	

class FoilEntry(Frame):
    def __init__(self, master):
    	Frame.__init__(self, master)
    	self.grid()
    	self.createWidgets()

    def createWidgets(self):
    	row_num = 0
        self.section_width_label = Label(self, text='Section width')
        self.section_width_label.grid(row=row_num, column=0)
        self.section_width_var = DoubleVar()
        self.section_width_input = Entry(self, textvariable=self.section_width_var ,width=15)
        self.section_width_input.grid(row=row_num, column=1)

    	row_num += 1
        self.section_thickness_label = Label(self, text='Maximum thickness')
        self.section_thickness_label.grid(row=row_num, column=0)
        self.section_thickness_var = DoubleVar()
        self.section_thickness_input = Entry(self, textvariable=self.section_thickness_var ,width=15)
        self.section_thickness_input.grid(row=row_num, column=1)

    	row_num += 1
        self.laminate_thickness_label = Label(self, text='Laminate thickness (per side)')
        self.laminate_thickness_label.grid(row=row_num, column=0)
        self.laminate_thickness_var = DoubleVar()
        self.laminate_thickness_input = Entry(self, textvariable=self.laminate_thickness_var ,width=15)
        self.laminate_thickness_input.grid(row=row_num, column=1)

    	row_num += 1
        self.regime_split_label = Label(self, text='Regime split point')
        self.regime_split_label.grid(row=row_num, column=0)
        self.regime_split_var = DoubleVar()
        self.regime_split_input = Scale(self, variable=self.regime_split_var, from_=0.8, to=1.0, orient=HORIZONTAL, resolution=0.01, length=150, sliderlength=20)
        self.regime_split_input.grid(row=row_num, column=1)

    	row_num += 1
        self.num_points_label = Label(self, text='Number of profile points')
        self.num_points_label.grid(row=row_num, column=0)
        self.num_points_var = DoubleVar()
        self.num_points_input = Scale(self, variable=self.num_points_var, from_=31, to=1001, orient=HORIZONTAL,  length=150, sliderlength=20)
        self.num_points_input.grid(row=row_num, column=1)

    	row_num += 1
        self.button_drawfoil = Button(self,text="Generate foil",command=self.drawFoil, bd=15)
        self.button_drawfoil.grid(row=row_num, column=0, columnspan=2)		

    def drawFoil(self):
    	self.canvas.delete("profile")

    	# variables:
    	#	- width
    	#	- max thickness
    	#	- laminate thickness (per side)
    	#	- regime split point
    	foil_W = self.section_width_var.get()
    	foil_T = self.section_thickness_var.get()
    	lam_T = self.laminate_thickness_var.get()
    	foil_split = self.regime_split_var.get()
    	foil_points = self.num_points_var.get()
    	self.canvas.create_line(0, 0, foil_points, foil_points, fill="white", tag="profile")


class FoilCanvas(GeoFrame):
    def __init__(self, master):
        self.canvas_options = {"width":500, "height":300, "bg":"black"}
        self.grid_options = {"grid_spacing": 50, "canW": 500, "canH": 300, "margin": 5}
        GeoFrame.__init__(self, master, self.canvas_options, self.grid_options)
        self.grid(row=0, column=0)
        self.canvas.create_line(0,0,100,100, fill="yellow")



app = Application()
app.master.title("Foil Generator")
app.mainloop()