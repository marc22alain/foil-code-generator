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


import Glib as G
import MC_defaults as MC
import simple_generators as SG
# END for local module imports


"""
Board blanks have relative (0,0) reference points.
These must be related to the spoil board's absolute coordinates...
...or make a prepping move to the blank's (0,0) and reset the machine's absolute origin.
But don't forget to record the magnitude of the origin reset so that it can be restored.

So, given that the machine has been roughly set to the blank's origin, make two sets of location holes.
The locating holes will be centered on the blank's nominal centerline.
Spacing from the first end is user-selected, as is the spacing between rows of holes.
"""

# USER SELECTIONS, specified in mm, and try to remember to put in the decimal point... floats are good
# (x,y)
blank_nominal = (900.0, 220.0)

# space from blank's origin y = 0
first_row_start = 50.0

# space from first row y
second_row_start = 800.0

blank_thickness = 25.0

bit_diameter = 6.35

safe_Z = 80.0

cut_per_pass = 3.0

file_name = "byte_blank_holes.ngc"

# END of user selections

# sanity checks
assert bit_diameter in MC.bits, "the specified bit diameter is not in the tool box"
assert bit_diameter < 8.0, "the specified bit diameter is too large"
assert blank_nominal[0] > (first_row_start + second_row_start + 10), "blank is too short"
assert blank_nominal[1] > 215, "blank is too narrow"
assert second_row_start in MC.spoil_board_spacings, "row spacing is not available"



def machineRow(safe_Z, blank_nominal, blank_thickness, cut_per_pass, bit_diameter):
    text = ""
    center_line = blank_nominal[1] / 2.0
    # magic number 100 is based on assumption that mounting holes are +/- 100mm from the centerline locating hole
    # mounting hole # 1
    text += G.G0_Y(center_line - 100)
    text += SG.bore_circle_ID(safe_Z, blank_thickness, cut_per_pass, 0,
              bit_diameter, 8.1)

    # centerline location hole
    text += G.G0_Y(center_line)
    text += SG.bore_circle_ID(safe_Z, blank_thickness, cut_per_pass, 0,
              bit_diameter, 12.7)

    # mounting hole # 2
    text += G.G0_Y(center_line + 100)
    text += SG.bore_circle_ID(safe_Z, blank_thickness, cut_per_pass, 0,
              bit_diameter, 8.1)
    return text


g_code = ""

g_code += SG.startProgram(MC.default_feed_rate)

g_code += G.G0_Z(safe_Z)

g_code += G.G0_X(first_row_start)

g_code += machineRow(safe_Z, blank_nominal, blank_thickness, cut_per_pass, bit_diameter)

g_code += G.G0_X(first_row_start + second_row_start)

g_code += machineRow(safe_Z, blank_nominal, blank_thickness, cut_per_pass, bit_diameter)

g_code += G.G0_X(0)

g_code += SG.endProgram()

print g_code

with open(file_name, 'w') as myFile:
    myFile.write(g_code)
