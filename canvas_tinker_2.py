import Tkinter as TK

can_W = 300
can_H = 350
margin = 5
grid_spacing = 50

assert can_W % grid_spacing == 0, "canvas width and grid spacing are incompatible"
assert can_H % grid_spacing == 0, "canvas height and grid spacing are incompatible"

master = TK.Tk()

w = TK.Canvas(master, width=(can_W + (2 * margin)), height=(can_H + (2 * margin)), bg="#aaaaaa")
w.pack()

# w.create_line(0, 0, 200, 100)
# w.create_line(0, 100, 200, 0, fill="red", dash=(4, 4))

# w.create_rectangle(50, 25, 150, 75, fill="blue")


def makeGrid(canvas, width, height, margin, grid_spacing):
	for i in xrange(1, width / grid_spacing):
		canvas.create_line((i * grid_spacing) + margin, margin,  (i * grid_spacing) + margin, height + margin, fill="#77aa19")
	for j in xrange(1, height / grid_spacing):
		canvas.create_line(margin, (j * grid_spacing) + margin, width + margin,  (j * grid_spacing) + margin)
	# canvas.create_line(10,10,width,10, fill="red")
	# canvas.create_line(10,height,width,height)
	# canvas.create_line(width,10,width,height)
	# canvas.create_line(10,10,10,height)

makeGrid(w, can_W, can_H, margin, grid_spacing)


TK.mainloop()