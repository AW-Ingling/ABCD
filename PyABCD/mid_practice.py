
from abcd_show import *
from abcd_table import *
from mid_practice_helpers import *
from mid_dialogs import *
import mid_practice_record

# TODO: Replace sys.exit() with assertions so that we still have state in the console; throw exceptions.


# KEY name variables resolved at runtime:
# SPACE_KEY

# Duration for which the probe appears in seconds, defined in E-Prime GetVersionImages
INITIAL_PROBE_DURATION_SECS = 0.350
INCREMENTED_PROBE_DURATION_SECS = 0.400
probe_duration_secs = INITIAL_PROBE_DURATION_SECS

# Get the stimulus bundle object which manages stimulus images, tables and text files for the project
stim_bundle = StimBundle("mid_practice")

# Load tables for the training loops

# TODO: Just load these int a dictionary at once
ifis_block_table = AbcdTable(stim_bundle, "IFISBlockList")
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

# Load tables for the second training loop
# E-Prime name: TimingBlockList
timing_block_table = AbcdTable(stim_bundle, "TimingBlockList")
period_list_table = AbcdTable(stim_bundle, "PeriodListTiming")
run_list_table = AbcdTable(stim_bundle, "RunListTiming")


# Instantiate the shower class which presents specified stimuli from the bundle and records results
shower = ShowMaker(stim_bundle)

# Get the operator input
screen_index = get_target_screen_index()
operator_table = get_inputs(lambda f_name: stim_bundle.data_file_for_name(f_name)[1], screen_index)
if operator_table is None:
    sys.exit()

# Create the data output spreadsheet and set some fields
output_record = mid_practice_record.MidPracticeRecord(stim_bundle.data_dir_path, operator_table['file_name'])
output_record.add_constant_column("DataFile.Basename", operator_table['file_name_without_extension'])
output_record.add_constant_column("Group", operator_table['session_number'])
output_record.add_constant_column("Handedness", operator_table['handedness'])
seesion_date, session_time = formatted_date_time()
output_record.add_constant_column("SessionDate", seesion_date)
output_record.add_constant_column("SessionTime", session_time)




# Open the stimulus window, fire up the IOHub engine to read key presses
screen_num = shower.setup()

# Get the display frame rate and put it in the output table
framerate_hz = shower.get_framerate_hz()
output_record.add_constant_column("Display.RefreshRate", round(framerate_hz, 3))


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
for trial_type_index in range(0, ifis_block_table.num_rows):

    # Give the user the instructions for one of the five practice trial types
    # TODO: Fix the cell_value function so that it accepts in index instead of ID
    instruction_1 = ifis_block_table.cell_value("Instruction1", trial_type_index + 1)
    instruction_2 = ifis_block_table.cell_value("Instruction2", trial_type_index + 1)
    text_subs_block_instr = {'Instruction1':instruction_1, 'Instruction2': instruction_2}
    shower.show("BlockInstruction", None, "SPACE_KEY", text_subs_block_instr)

    # Show each trial type type two times
    list_name = ifis_block_table.cell_value("ListName", trial_type_index + 1)
    task = ifis_block_table.cell_value("Task", trial_type_index + 1)
    trial_table = tables[list_name]
    for trial_index in range(0,trial_table.num_rows):

        # add a new row to the output table and fill in some values
        output_record.add_new_row()
        output_record.add_cell_value_to_row("ProbeDuration", secs_to_msecs(probe_duration_secs))
        output_record.add_cell_value_to_row("Block", trial_type_index + 1)
        output_record.add_cell_value_to_row("IFISBlockList", trial_type_index + 1)
        output_record.add_cell_value_to_row("IFISBlockList.Sample", trial_type_index + 1)
        output_record.add_cell_value_to_row("IFISBlockList.Cycle", 1)

        output_record.add_cell_value_to_rows(mid_practice_record.first_trails_nulls, "NULL")


        # dynamically reference file names for this trials stimuli
        cue_file_name = trial_table.cell_value("Cue", trial_index + 1)
        probe_file_name = trial_table.cell_value("Probe", trial_index + 1)

        # present the cue, the colored shape stating reward value,  for 2000 msecs = 2 seconds
        shower.show_file(cue_file_name, 2.0)

        # present the crosshairs for 2000 msecs = 2 seconds
        #TODO: Record key presses and return them even if non are filtered int
        stim_record_anticipation= shower.show("Anticipation", 2.0, "SPACE_KEY")

        # present the probe, the solid black shape for 350 msecs = 0.350 seconds
        stim_record_probe = shower.show_file(probe_file_name, probe_duration_secs, "SPACE_KEY")
        reaction_time = stim_record_probe.first_keydown_delay_secs

        # lookup text strings according to trial state and response, generate dyanamic message
        response_text, prbacc_flag = check_response_inline(stim_record_anticipation.was_key_pressed,
                                                      stim_record_probe.was_key_pressed)
        tbl_condition = trial_table.cell_value("Condition", trial_index + 1)
        result_text = result_inline(tbl_condition, prbacc_flag)
        text_subs_feedback = {"ResponseCheck" : response_text, "Result" : result_text}
        shower.show("Feedback", 1.650, [], text_subs_feedback)

        output_record.add_cell_value_to_row("Instruction1", instruction_1)
        output_record.add_cell_value_to_row("Instruction2", instruction_2)
        output_record.add_cell_value_to_row("ListName", list_name)
        output_record.add_cell_value_to_row("Procedure[Block]", "BlockProc")
        output_record.add_cell_value_to_row("Running[Block]", "IFISBlockList")
        output_record.add_cell_value_to_row("Task", task)
        output_record.add_cell_value_to_row("Trial", 1)
        output_record.add_cell_value_to_row("PeriodList", 1)
        output_record.add_cell_value_to_row("PeriodList.Cycle", trial_type_index + 1)
        output_record.add_cell_value_to_row("PeriodList.Sample", trial_type_index + 1)
        output_record.add_cell_value_to_row("Procedure[Trial]", "TrialProc")
        output_record.add_cell_value_to_row("Running[Trial]", "PeriodList")









        # TODO: Verify that the response window duration should be same same as the probe duration


        # Write the response time to the output record
        output_record.add_cell_value_to_row("Probe.RT", secs_to_msecs(reaction_time))

        # write the response check and result check messages to the output record
        output_record.add_cell_value_to_row("ResponseCheck", response_text)
        output_record.add_cell_value_to_row("Result", result_text)

# E-Prime name: PartOneEndText
shower.show("PartOneEndText", None, "SPACE_KEY")


# Begin the TimingBlockList/BlocProcTiming list/procedure training loop.
for procedure_index in range(0, timing_block_table.num_rows):

    # fetch the procdure name from the table
    procedure_name = timing_block_table.cell_value("Procedure", procedure_index + 1)

    # E-Prime name: BlockInstructionsTiming
    shower.show("BlockInstructionsTiming", None, "SPACE_KEY")

    # NOTE:  The PeriodListTiming table only specifies to run the two procedures under it only once each.
    #        It is uncessary here becasue we can embed those under the same loop without referencing them in a table.

    # E-prime name: PrepTime
    shower.show("PrepTime", 5)

    # E-Prime name: InitRunVar
    eprime_summation = EprimeSummation()

    # E-Prime name: TrialProcTiming
    for run_list_index in range(0, run_list_table.num_rows):

        # add a new row to the output table
        output_record.add_new_row()
        output_record.add_cell_value_to_row("ProbeDuration", secs_to_msecs(probe_duration_secs))
        output_record.add_cell_value_to_rows(mid_practice_record.second_trails_nulls, "NULL")

        # E-Prime name: Cue
        cue_file_name = run_list_table.cell_value("Cue", run_list_index + 1)
        shower.show_file(cue_file_name, 2.0)

        # E-Prime name: Anticipation
        stim_record_anticipation = shower.show("Anticipation", 2.0, "SPACE_KEY")

        # E-Prime name: Probe
        probe_file_name= run_list_table.cell_value("Probe", run_list_index + 1)
        stim_record_probe = shower.show_file(probe_file_name, probe_duration_secs, "SPACE_KEY")
        reaction_time = stim_record_probe.first_keydown_delay_secs
        eprime_summation.add_observation_secs(reaction_time)

        # Write the response time to the output record
        output_record.add_cell_value_to_row("Probe.RT", secs_to_msecs(reaction_time))

        # E-Prime name: CheckResponse
        # lookup text strings according to trial state and response, generate dynamic message
        response_text, prbacc_flag = check_response_inline(stim_record_anticipation.was_key_pressed,
                                                           stim_record_probe.was_key_pressed)

        # E-Prime name: Result
        # Lookup the "Condition" key value then use that value to get the result text
        #tbl_condition = run_list_table.cell_value("Condition", trial_index + 1)
        tbl_condition = run_list_table.cell_value("Condition", run_list_index + 1)
        result_text = result_inline(tbl_condition, prbacc_flag)

        # E-Prime name: Feedback
        text_subs_feedback = {"ResponseCheck": response_text, "Result": result_text}
        shower.show("Feedback", 1.650, [], text_subs_feedback)

        # write the response check and result check messages to the output record
        output_record.add_cell_value_to_row("ResponseCheck", response_text)
        output_record.add_cell_value_to_row("Result", result_text)

    # E-Prime name: CheckRT
    mean_rt = eprime_summation.mean_ms
    if mean_rt > 0:
        break
    else:
        probe_duration_secs = INCREMENTED_PROBE_DURATION_SECS


# E-Prime name Goodbye
shower.show("Goodbye", None, "SPACE_KEY")

# E-Prime name DisplayPracticeRT
int_new_rt = eprime_summation.user_rt_ms
text_subs_rt = {"IntNewRT" : str(int_new_rt)}
shower.show("DisplayPracticeRT", None, "SPACE_KEY", text_subs_rt)

# store the data table
output_record.save()


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

