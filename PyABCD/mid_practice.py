
from abcd_show import *
from abcd_table import *

# TODO: Replace sys.exit() with assertions so that we still have state in the console; throw exceptions.

# KEY name variables resolved at runtime:
# SPACE_KEY

# Duration for which the probe appears in seconds, defined in E-Prime GetVersionImages
INITIAL_PROBE_DURATION = 0.350
probe_duration = INITIAL_PROBE_DURATION

# Get the stimulus bundle object which manages stimulus images, tables and text files for the project
stim_bundle = StimBundle("mid_practice")

# Load tables
# TODO: Just load these int a dictionary at once
timing_block_table = AbcdTable(stim_bundle, "TimingBlockList")
lose_big_table = AbcdTable(stim_bundle, "LoseBig")
lose_small_table = AbcdTable(stim_bundle, "LoseSmall")
neutral_table = AbcdTable(stim_bundle, "Neutral")
win_big_table = AbcdTable(stim_bundle, "WinBig")
win_small_table = AbcdTable(stim_bundle, "WinSmall")

# Create a mapping of table names to tables so that tables can be references by their names from other tables
tables = {"LoseBig": lose_big_table,
          "LoseSmall": lose_small_table,
          "Neutral": neutral_table,
          "WinBig": win_big_table,
          "WinSmall": win_small_table}


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

# E-Prime name: BlockInstruction
for trial_type_index in range(0,timing_block_table.num_rows):

    # Give the user the instructions for one of the five practice trial types
    # TODO: Fix the cell_value function so that it accepts in index instead of ID
    instruction_1 = timing_block_table.cell_value("Instruction1", trial_type_index + 1)
    instruction_2 = timing_block_table.cell_value("Instruction2", trial_type_index + 1)
    text_subs = {'Instruction1':instruction_1, 'Instruction2': instruction_2}
    shower.show("BlockInstruction", None, "SPACE_KEY", text_subs)

    # Show each trial type type two times
    trial_table = tables[timing_block_table.cell_value("ListName", trial_type_index + 1)]
    for trial_index in range(0,trial_table.num_rows):
        # dynamically reference file names for this trials stimuli
        cue_file_name = trial_table.cell_value("Cue", trial_index + 1)
        probe_file_name = trial_table.cell_value("Probe", trial_index + 1)
        # present the cue, the colored shape stating reward value,  for 2000 msecs = 2 seconds
        shower.show_file(cue_file_name, 2.0)
        # present the crosshairs for 2000 msecs = 2 seconds
        #TODO: Record key presses and return them even if non are filtered int
        stim_record_anticipation= shower.show("Anticipation", 2.0)
        # present the probe, the solid black shape for 350 msecs = 0.350 seconds
        stim_record_probe = shower.show_file(probe_file_name, probe_duration, "SPACE_KEY")
        # check if the user met the deadline
        # TODO: Verify that the response window is the same as the probe duration
        met_dealine = stim_record.was_keypress_before_timeout



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

