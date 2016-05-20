from Tkinter import *


class GeoFrame(Frame):
    def __init__(self, master, init_options, grid_options):
        Frame.__init__(self, master, bd=5)
        self.grid()
        self.canvas = Canvas(self, init_options)
        self.canvas.grid(row=0, column=0)
        self.drawCanvasGrid(grid_options)


    def drawCanvasGrid(self, grid_options):
    	# self.canvas.create_line(0, 100, 200, 0, fill="red", dash=(4, 4))
    	margin = grid_options["margin"]
    	width = grid_options["canW"]
    	height = grid_options["canH"]
    	grid_spacing = grid_options["grid_spacing"]
    	for i in xrange(1, width / grid_spacing):
			self.canvas.create_line((i * grid_spacing) + margin, margin,  (i * grid_spacing) + margin, height + margin, fill="#888")
    	for j in xrange(1, height / grid_spacing):
			self.canvas.create_line(margin, (j * grid_spacing) + margin, width + margin,  (j * grid_spacing) + margin, fill="#888")