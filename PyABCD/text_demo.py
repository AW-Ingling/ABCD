# text_demo.py
#
# Experiment with drawing some text to get the ABCD text_display module to work right

from psychopy import visual, core
from abcd_text import *



# Open the window and draw the sample text
win = visual.Window(screen=1, fullscr=True, units='pix')
message = "Hello\n\nTree\n\nBanana"
font_size_points = 40
font_size_pixels = points_to_pixels(font_size_points)
block = TextBlock(win, message, "verdana", font_size_pixels)
block.format()
block.draw()
win.flip()
core.wait(5.0)
win.close()


# message = make_abcd_text(win, "Hello\n\nTree\n\nBanana", 50)
# message.draw()
# win.flip()
# core.wait(5.0)
# win.close()


