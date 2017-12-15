
from psychopy import visual, core, monitors
from abcd_window import *
from abcd_show import *
from stim_bundle import *

# Name input characters.
SPACE_KEY = ' '

# Init IOHUB indirectly
Presenter.setup()

# Create an array to hold all of the presentation data
stim_records = []

# Get the stimulus bundle
stim_bundle = StimBundle("mid_practice")

# Open the window for the stimuli
w = open_stimulus_window()

# TODO: Put that all in one line by wrapping Presenter in a closure which includes the bundle and also implementing a
# TODO: ...class method on Presenter which crates and instance and runs show
# TODO: ...also call setup

# Present the title page
p = Presenter(w, stim_bundle, "MID_Practice_TitlePage", None, SPACE_KEY)
record = p.show_image()
stim_records.append(record)

# Close the window
w = close_stimulus_window()

