# text_wrap_test.py
#
# Experiments with text wrapping because the default behavior is "wrong"

#from psychopy import visual, core
from abcd_show import *
from abcd_text import *



# Open the window and draw the sample text
win = visual.Window(screen=1, fullscr=True, units='pix')
message = "The quick brown fox jumps over the lazy dog\n"
font_size_points = 18
font_size_pixels = points_to_pixels(font_size_points)
block = TextBlock(win, message, "verdana", font_size_pixels)
block.format()
block.draw()
win.flip()
core.wait(5.0)
win.clearBuffer()
win.flip()
core.wait(1.0)
text_stim = visual.TextStim(win,
                            font="verdana",
                            color='Black',
                            units='pix',
                            height= font_size_pixels,
                            text="The quick brown fox jumps over the lazy dog\n",
                            wrapWidth=1920)
text_stim.draw()
win.flip()
core.wait(5.0)

win.close()



