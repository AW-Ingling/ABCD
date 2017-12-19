
from psychopy import visual, core, monitors
from abcd_window import *
from abcd_show import *
from stim_bundle import *

# Name input characters.
SPACE_KEY = ' '

# Init IOHUB indirectly
#Show.setup()


# Instantiate the shower class which presents specified stimuli from the bundle and records results
shower = ShowMaker("mid_practice")

# Open the stimulus window, fire up the IOHub engine to read key presses
shower.setup()

# Display the first stimulus, wait for keypress, record timing and response into a record
shower.show("MID_Practice_TitlePage", None, SPACE_KEY)

# Close the stimulus window, shutdown the IOHUb engine used to read key presses.
shower.shutdown()

# Print the raw fields from the records
shower.print_records()


# Open the window for the stimuli
#w = open_stimulus_window()

# TODO: Put that all in one line by wrapping Presenter in a closure which includes the bundle and also implementing a
# TODO: ...class method on Presenter which creates and instance and runs show
# TODO: ...also call setup

# 1. Present the title page, wait for space bar
#p = Show(w, stim_bundle, "MID_Practice_TitlePage", None, SPACE_KEY)
#record = p.show()
#stim_records.append(record)

# Close the window
#w = close_stimulus_window()

