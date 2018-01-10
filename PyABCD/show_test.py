

from abcd_show import *
from abcd_table import *

# Get the stimulus bundle object which manages stimulus images, tables and text files for the project
stim_bundle = StimBundle("mid_practice")

# Instantiate the shower class which presents specified stimuli from the bundle and records results
shower = ShowMaker(stim_bundle)

# Open the stimulus window, fire up the IOHub engine to read key presses
shower.setup()

# Test the key input parameter alone
shower.show_file("Neutral.BMP", None, "SPACE_KEY")

# Test the timout parameter alone
shower.show_file("WinBig.BMP", 2.0)

# Test the timeout parameter in combination with the key input paremter
shower.show_file("LoseSmall.BMP", 3.0, "SPACE_KEY")

