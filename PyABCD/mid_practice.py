
from mid_dialogs import *  # for some unknown reason this must be imported first or the dialogs are not seen.
from abcd_show import *
from abcd_table import *
from mid_practice_helpers import *
import mid_practice_record
import abcd_random


# TODO: Replace sys.exit() with assertions so that we still have state in the console; throw exceptions.

# init our random number generator so so that we can get the seed for the table
rand_gen = abcd_random.ABCDRandom()

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

# Define exit key sequence.  For definition of modifier key strings see:
# http://www.psychopy.org/api/iohub/device/keyboard.html#keyboard-events
exit_detector = ExitDetector("q", ["lctrl", "rctrl"])

# Instantiate the shower class which presents specified stimuli from the bundle and records results
shower = ShowMaker(stim_bundle, exit_detector)


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
output_record.add_constant_column("NARGUID", operator_table['subject_id'])
seesion_date, session_time = formatted_date_time()
output_record.add_constant_column("SessionDate", seesion_date)
output_record.add_constant_column("SessionTime", session_time)


# Open the stimulus window, fire up the IOHub engine to read key presses
screen_num = shower.setup()


# Get the display frame rate and put it in the output table
framerate_hz = shower.get_framerate_hz()
output_record.add_constant_column("Display.RefreshRate", round(framerate_hz, 3))
output_record.add_constant_column("RandomSeed", rand_gen.seed)

# mark start time for timers which generates values for output columns:
#  - Probe.OnsetDelay
#  - Probe.OnsetTime
#  - Probe.OnsetToOnsetTime
# TODO: Figure out where this should really go.
mark_start_time()

try:

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
    # Init variables used only for output to spreadsheet.
    runlist_sample_counter = 1  # used only for an output table column
    periodListTiming_sample = 1

    for trial_index in range(0, ifis_block_table.num_rows):

        # Give the user the instructions for one of the five practice trial types
        # TODO: Fix the cell_value function so that it accepts in index instead of ID
        instruction_1 = ifis_block_table.cell_value("Instruction1", trial_index + 1)
        instruction_2 = ifis_block_table.cell_value("Instruction2", trial_index + 1)
        text_subs_block_instr = {'Instruction1':instruction_1, 'Instruction2': instruction_2}
        shower.show("BlockInstruction", None, "SPACE_KEY", text_subs_block_instr)

        # Show each trial type type two times
        list_name = ifis_block_table.cell_value("ListName", trial_index + 1)
        task = ifis_block_table.cell_value("Task", trial_index + 1)
        trial_table = tables[list_name]
        for subtrial_index in range(0, trial_table.num_rows):

            # add a new row to the output table and fill in some values
            output_record.add_new_row()
            output_record.add_cell_value_to_row("ProbeDuration", secs_to_msecs(probe_duration_secs))
            output_record.add_cell_value_to_row("Block", trial_index + 1)
            output_record.add_cell_value_to_row("IFISBlockList", trial_index + 1)
            output_record.add_cell_value_to_row("IFISBlockList.Sample", trial_index + 1)
            output_record.add_cell_value_to_row("IFISBlockList.Cycle", 1)

            output_record.add_cell_value_to_columns(mid_practice_record.first_trails_nulls, "NULL")


            # dynamically reference file names for this trials stimuli
            cue_file_name = trial_table.cell_value("Cue", subtrial_index + 1)
            probe_file_name = trial_table.cell_value("Probe", subtrial_index + 1)

            # present the cue, the colored shape stating reward value,  for 2000 msecs = 2 seconds
            shower.show_file(cue_file_name, 2.0)

            # present the crosshairs for 2000 msecs = 2 seconds
            #TODO: Record key presses and return them even if non are filtered int
            stim_record_anticipation= shower.show("Anticipation", 2.0, "SPACE_KEY", None, False)

            # present the probe, the solid black shape for 350 msecs = 0.350 seconds
            stim_record_probe = shower.show_file(probe_file_name, probe_duration_secs, "SPACE_KEY", None, False)
            reaction_time = stim_record_probe.first_keydown_delay_secs

            # lookup text strings according to trial state and response, generate dyanamic message
            response_text, prbacc_flag = check_response_inline(stim_record_anticipation.was_key_pressed,
                                                               stim_record_probe.was_key_pressed)
            tbl_condition = trial_table.cell_value("Condition", subtrial_index + 1)
            result_text = result_inline(tbl_condition, prbacc_flag)
            text_subs_feedback = {"ResponseCheck" : response_text, "Result" : result_text}
            shower.show("Feedback", 1.650, [], text_subs_feedback)


            output_record.add_cell_value_to_row("Probe.OnsetDelay", stim_record_probe.onset_delay_msecs(stim_record_anticipation))
            output_record.add_cell_value_to_row("Probe.OnsetTime", stim_record_probe.onset_time_msecs)
            output_record.add_cell_value_to_row("Probe.OnsetToOnsetTime", stim_record_probe.onset_to_onset_time_msecs)
            output_record.add_cell_value_to_row("Probe.DurationError", stim_record_probe.duration_error_msecs(probe_duration_secs))

            output_record.add_cell_value_to_row("Instruction1", instruction_1)
            output_record.add_cell_value_to_row("Instruction2", instruction_2)
            output_record.add_cell_value_to_row("ListName", list_name)
            output_record.add_cell_value_to_row("Procedure[Block]", "BlockProc")
            output_record.add_cell_value_to_row("Running[Block]", "IFISBlockList")
            output_record.add_cell_value_to_row("Task", task)
            output_record.add_cell_value_to_row("Trial", 1)
            output_record.add_cell_value_to_row("PeriodList", 1)
            output_record.add_cell_value_to_row("PeriodList.Cycle", trial_index + 1)
            output_record.add_cell_value_to_row("PeriodList.Sample", trial_index + 1)
            output_record.add_cell_value_to_row("Procedure[Trial]", "TrialProc")
            output_record.add_cell_value_to_row("Running[Trial]", "PeriodList")

            output_record.add_cell_value_to_row("SubTrial", subtrial_index + 1)
            output_record.add_cell_value_to_row("Condition", tbl_condition)
            output_record.add_cell_value_to_row("Cue", cue_file_name)
            output_record.add_cell_value_to_row("LoseBig", condition_column_value("LoseBig", task, subtrial_index))
            output_record.add_cell_value_to_row("LoseSmall", condition_column_value("LoseSmall", task, subtrial_index))
            output_record.add_cell_value_to_row("Neutral", condition_column_value("Neutral", task, subtrial_index))
            output_record.add_cell_value_to_row("prbacc", prbacc_flag)
            output_record.add_cell_value_to_row("Probe", probe_file_name)

            # DurationError: "difference between the expected duration and actual duration"
            #    output_record.add_cell_value_to_row("Probe.DurationError", )

            # OnsetDelay: "difference between the target onset time and the actual onset time"
            #    output_record.add_cell_value_to_row("Probe.OnsetDelay", )

            # OnsetTime: "timestamp of stimulus onset (ms)"
            #    output_record.add_cell_value_to_row("Probe.OnsetTime", )

            # OnsetToOnsetTime: "difference between the next and this onset time"
            # Typical values for this are 433 wich is the sum of column Probe.OnsetDelay value, 83, and ProbeDuration[Session],
            # 350.
            #
            #    output_record.add_cell_value_to_row("Probe.OnsetToOnsetTime", )


            output_record.add_cell_value_to_row("Probe.RESP", probe_resp_value(prbacc_flag))

            output_record.add_cell_value_to_row("Procedure[SubTrial]", "RewardProc")
            output_record.add_cell_value_to_row("ResponseCheck", response_text)
            output_record.add_cell_value_to_row("Result", result_text)
            output_record.add_cell_value_to_row("RunList", 1)
            output_record.add_cell_value_to_row("RunList.Cycle", trial_index + 1)
            output_record.add_cell_value_to_row("RunList.Sample", runlist_sample_counter)
            output_record.add_cell_value_to_row("RunListTiming", "NULL")
            output_record.add_cell_value_to_row("RunListTiming.Cycle", "NULL")
            output_record.add_cell_value_to_row("RunListTiming.Sample", "NULL")
            output_record.add_cell_value_to_row("Running[SubTrial]", "RunList")
            output_record.add_cell_value_to_row("WinBig", condition_column_value("WinBig", task, subtrial_index))
            output_record.add_cell_value_to_row("WinSmall", condition_column_value("WinSmall", task, subtrial_index))

            runlist_sample_counter += 1
            # TODO: Verify that the response window duration should be same same as the probe duration


            # Write the response time to the output record
            output_record.add_cell_value_to_row("Probe.RT", secs_to_msecs(reaction_time))

            # write the response check and result check messages to the output record
            output_record.add_cell_value_to_row("ResponseCheck", response_text)
            output_record.add_cell_value_to_row("Result", result_text)

    # E-Prime name: PartOneEndText
    shower.show("PartOneEndText", None, "SPACE_KEY")



    # Begin the TimingBlockList/BlocProcTiming list/procedure training loop.
    block_counter = trial_index + 2     # add one to increment and one to convert from 0-indexing to 1-indexing
    prac_run_counter = 1                # used only for table output column "BlockTitle"
    periodListTiming_sample = 0         # only used for the eponymous output data column
    for procedure_index in range(0, timing_block_table.num_rows):

        # fetch the procdure name from the table
        procedure_name = timing_block_table.cell_value("Procedure", procedure_index + 1)

        # E-Prime name: BlockInstructionsTiming
        shower.show("BlockInstructionsTiming", None, "SPACE_KEY")

        # NOTE:  The PeriodListTiming table only specifies to run the two procedures under it only once each.
        #        It is unnecessary here because we can embed those under the same loop without referencing them in a table.

        # E-prime name: PrepTime
        shower.show("PrepTime", 5)

        # E-Prime name: InitRunVar
        eprime_summation = EprimeSummation()

        # The rule for incrementing is set to match the E-Prime output for this varaible's column
        periodListTiming_sample += 1

        # Create a null line between the first and scecond training loops to match the output from E-Prime
        # Columns for the dummy row are filled in by four methods:
        # - dummy constant columns defined in module abcd_table
        # - constant columns defined above in this script, mid_practice
        # - second trail nulls set below with keys defined in module abcd_table
        # - inter-training nulls defined in module abcd_table
        output_record.add_new_row()
        output_record.add_cell_value_to_columns(mid_practice_record.second_trails_nulls, "NULL")
        output_record.add_cell_value_to_columns(mid_practice_record.inter_test_loop_nulls, "NULL")
        output_record.add_cell_value_to_row("ProbeDuration", secs_to_msecs(probe_duration_secs))
        output_record.add_cell_value_to_row("Block", block_counter)
        output_record.add_cell_value_to_row("BlockTitle", counter_to_block_title(prac_run_counter))
        output_record.add_cell_value_to_row("NameOfPeriodList", "PeriodList")
        output_record.add_cell_value_to_row("Periods", 2)           # TODO: check that this does not turn to 3 on 2nd pass
        output_record.add_cell_value_to_row("Procedure[Block]", "BlockProc")
        output_record.add_cell_value_to_row("Running[Block]", "TimingBlockList")
        output_record.add_cell_value_to_row("TimingBlockList", prac_run_counter)
        output_record.add_cell_value_to_row("TimingBlockList.Cycle", 1)
        output_record.add_cell_value_to_row("TimingBlockList.Sample", prac_run_counter)
        output_record.add_cell_value_to_row("Trial", 1)
        output_record.add_cell_value_to_row("PeriodListTiming", 1)
        output_record.add_cell_value_to_row("PeriodListTiming.Cycle", prac_run_counter)
        output_record.add_cell_value_to_row("PeriodListTiming.Sample", periodListTiming_sample)
        output_record.add_cell_value_to_row("Procedure[Trial]", "PrepProcTiming")
        output_record.add_cell_value_to_row("Running[Trial]", "PeriodListTiming")

        # The rule for incrementing is set to match the E-Prime output for this varaible's column
        periodListTiming_sample += 1

        # E-Prime name: TrialProcTiming
        for run_list_index in range(0, run_list_table.num_rows):

            # add a new row to the output table
            output_record.add_new_row()
            output_record.add_cell_value_to_row("ProbeDuration", secs_to_msecs(probe_duration_secs))
            output_record.add_cell_value_to_columns(mid_practice_record.second_trails_nulls, "NULL")

            # E-Prime name: Cue
            cue_file_name = run_list_table.cell_value("Cue", run_list_index + 1)
            shower.show_file(cue_file_name, 2.0)

            # E-Prime name: Anticipation
            stim_record_anticipation = shower.show("Anticipation", 2.0, "SPACE_KEY", None, False)

            # E-Prime name: Probe
            probe_file_name= run_list_table.cell_value("Probe", run_list_index + 1)
            stim_record_probe = shower.show_file(probe_file_name, probe_duration_secs, "SPACE_KEY", None, False)
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


            # write output data table columns
            output_record.add_cell_value_to_row("Block", block_counter)
            output_record.add_cell_value_to_row("BlockTitle", counter_to_block_title(prac_run_counter))
            output_record.add_cell_value_to_row("IFISBlockList", "NULL")
            output_record.add_cell_value_to_row("IFISBlockList.Cycle", "NULL")
            output_record.add_cell_value_to_row("IFISBlockList.Sample", "NULL")
            output_record.add_cell_value_to_row("Instruction1", "NULL")
            output_record.add_cell_value_to_row("Instruction2", "NULL")
            output_record.add_cell_value_to_row("ListName", "NULL")
            output_record.add_cell_value_to_row("NameOfPeriodList", "PeriodList")
            output_record.add_cell_value_to_row("Periods", 2)
            output_record.add_cell_value_to_row("Procedure[Block]", "BlockProcTiming")
            output_record.add_cell_value_to_row("Running[Block]", "TimingBlockList")
            output_record.add_cell_value_to_row("Task", "NULL")
            output_record.add_cell_value_to_row("TimingBlockList", prac_run_counter)
            output_record.add_cell_value_to_row("TimingBlockList.Cycle", 1)
            output_record.add_cell_value_to_row("TimingBlockList.Sample", prac_run_counter)
            output_record.add_cell_value_to_row("Trial", 2)
            output_record.add_cell_value_to_row("PeriodList", "NULL")
            output_record.add_cell_value_to_row("PeriodList.Cycle", "NULL")
            output_record.add_cell_value_to_row("PeriodList.Sample", "NULL")
            output_record.add_cell_value_to_row("PeriodListTiming", 2)
            output_record.add_cell_value_to_row("PeriodListTiming.Cycle", prac_run_counter)
            output_record.add_cell_value_to_row("PeriodListTiming.Sample", periodListTiming_sample)
            output_record.add_cell_value_to_row("Procedure[Trial]", "PrepProcTiming")
            output_record.add_cell_value_to_row("Running[Trial]", "PeriodListTiming")
            output_record.add_cell_value_to_row("SubTrial", prac_run_counter)
            output_record.add_cell_value_to_row("Anticipation.RESP", "")
            output_record.add_cell_value_to_row("Condition", tbl_condition)
            output_record.add_cell_value_to_row("Cue", cue_file_name)
            output_record.add_cell_value_to_row("LoseBig", "NULL")
            output_record.add_cell_value_to_row("LoseSmall", "NULL")
            output_record.add_cell_value_to_row("Neutral", "NULL")
            output_record.add_cell_value_to_row("prbacc", prbacc_flag)
            output_record.add_cell_value_to_row("Probe", probe_file_name)
            #    output_record.add_cell_value_to_row("Probe.ACC", )

            output_record.add_cell_value_to_row("Probe.OnsetDelay", stim_record_probe.onset_delay_msecs(stim_record_anticipation))
            output_record.add_cell_value_to_row("Probe.OnsetTime", stim_record_probe.onset_time_msecs)
            output_record.add_cell_value_to_row("Probe.OnsetToOnsetTime", stim_record_probe.onset_to_onset_time_msecs)
            output_record.add_cell_value_to_row("Probe.DurationError", stim_record_probe.duration_error_msecs(probe_duration_secs))

            output_record.add_cell_value_to_row("Probe.RESP", probe_resp_value(prbacc_flag))
            output_record.add_cell_value_to_row("Procedure[SubTrial]", "RewardProcTiming")
            output_record.add_cell_value_to_row("ResponseCheck", response_text)
            output_record.add_cell_value_to_row("Result", result_text)
            output_record.add_cell_value_to_row("RunList", "NULL")
            output_record.add_cell_value_to_row("RunList.Cycle", "NULL")
            output_record.add_cell_value_to_row("RunList.Sample", "NULL")
            output_record.add_cell_value_to_row("RunListTiming", prac_run_counter)
            output_record.add_cell_value_to_row("RunListTiming.Cycle", run_list_index + 1)
            output_record.add_cell_value_to_row("RunListTiming.Sample", prac_run_counter)
            output_record.add_cell_value_to_row("WinBig", "NULL")
            output_record.add_cell_value_to_row("WinSmall", "NULL")

            prac_run_counter += 1

        # E-Prime name: CheckRT
        mean_rt = eprime_summation.mean_ms
        if mean_rt > 0:
            break
        else:
            probe_duration_secs = INCREMENTED_PROBE_DURATION_SECS
            block_counter += 1

except UserExitRequest:
    shower.show_text("Exit command detected.  Press space bar to exit", None, "SPACE_KEY")

else:
    # E-Prime name Goodbye
    shower.show("Goodbye", None, "SPACE_KEY")

    # E-Prime name DisplayPracticeRT
    int_new_rt = eprime_summation.int_user_rt_ms
    text_subs_rt = {"IntNewRT" : str(int_new_rt)}
    shower.show("DisplayPracticeRT", None, "SPACE_KEY", text_subs_rt)

    # TODO: verify that the NewRT and IntNewRT values here are the ones which include stdev; In E-Prime the final message
    # TODO: ...should match the table column
    # The final calculated values for NewRT and IntNewRT fill every row in the E-Prime output
    new_rt = eprime_summation.user_rt_ms
    output_record.fill_column_data("NewRT", new_rt)
    output_record.fill_column_data("IntNewRT", int_new_rt)


finally:


    # Store the output spreadsheet
    # If the data is incomplete because we exited early then the "NewRT" and "IntNewRT" columns will not be present.
    output_record.save()

    # Close the stimulus window, shutdown the IOHUb engine used to read key presses.
    shower.shutdown()

