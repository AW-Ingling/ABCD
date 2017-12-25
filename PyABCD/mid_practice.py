
from abcd_show import *
from abcd_table import *


# Init IOHUB indirectly
#Show.setup()

# KEY name variables resolved at runtime:
# SPACE_KEY

# Get the stimulus bundle object which manages stimulus images, tables and text files for the project
stim_bundle = StimBundle("mid_practice")

# Load the table for a loop
timing_block_table = AbcdTable(stim_bundle, "TimingBlockList")

# Instantiate the shower class which presents specified stimuli from the bundle and records results
shower = ShowMaker(stim_bundle)

# Open the stimulus window, fire up the IOHub engine to read key presses
shower.setup()

# Display image/text stimuli, wait for keypresses, record timing and response into records


# E-Prime name: TitlePage
shower.show("TitlePage", None, "SPACE_KEY")

# E-Prime name: IntroShapes
shower.show("IntroShapes", None, "SPACE_KEY")

# E-Prime name: WinSml
shower.show("WinSmall", None, "SPACE_KEY")

# E-Prime name: WinLrg
shower.show("WinBig", None, "SPACE_KEY")

# E-Prime name: LoseSml
shower.show("LoseSmall", None, "SPACE_KEY")

# E-Prime name: LoseLrg
shower.show("LoseBig", None, "SPACE_KEY")

# E-Prime name: Neut
shower.show("Neutral", None, "SPACE_KEY")

# E-Prime name: ShapeFixInstruct
shower.show("ShapeFixInstruct", None, "SPACE_KEY")

# E-Prime name: IntroProbes
shower.show("IntroProbes", None, "SPACE_KEY")

# E-Prime name: Winprb
shower.show("WinProbe", None, "SPACE_KEY")

# E-Prime name: Loseprb
shower.show("LoseProbe", None, "SPACE_KEY")

# E-Prime name: NeutPrb
shower.show("NeutralProbe", None, "SPACE_KEY")

# E-Prime name: Probes2
shower.show("Probes2", None, "SPACE_KEY")

# TODO: This is the begining of the IFIS blocklist.












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

