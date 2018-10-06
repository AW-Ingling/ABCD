

# References:
#
# Keyboard input in E-Prime:
# http://www.e-primer.com/2015/06/special-keys-in-e-prime.html
#
#

from mid_dialogs import *
from abcd_versions import *
from abcd_show import *
from abcd_table import *
from mid_scanner_helpers import *
import mid_scanner_record
import abcd_random


# TODO: Replace SPACE_KEY with variable "allowed" set to "12" (whatever that means) to match E-Prime scanner version.
# TODO: Figure out what "PreRelease" parameter in E-Prime is match its behavior here.
# TODO: Confirm that mark_time() command starts at the right place.

# define the experiment and scanner type
version_keeper.assign_experiment_types(ExperimentType.mid, ScannerType.ge)

# init our random number generator so so that we can get the seed for the table
rand_gen = abcd_random.ABCDRandom()

# Get the stimulus bundle object which manages stimulus images, tables and text files for the project
stim_bundle = StimBundle("mid_scanner")

# Load tables
scanner_waiting_table = AbcdTable(stim_bundle, version_keeper.waiting_table_file_name())
period_list_table = AbcdTable(stim_bundle, "PeriodList")
block_list_table = AbcdTable(stim_bundle, "BlockList")
run_list_table =  AbcdTable(stim_bundle, "RunList")

# Get the operator input
screen_index = get_target_screen_index()
record_filename_maker = make_record_file_name_maker(stim_bundle)
operator_table = get_mid_scanner_inputs(record_filename_maker, screen_index)
if operator_table is None:
    sys.exit()

# Fetch the stimulus table according to the user input value for trial_order_version
block_file_names = []
block_file_names.append(time_version_file_name(0, operator_table["trial_order_version"]))
block_file_names.append(time_version_file_name(1, operator_table["trial_order_version"]))
block_tables = []
block_tables.append(AbcdTable(stim_bundle, block_file_names[0]))
block_tables.append(AbcdTable(stim_bundle, block_file_names[1]))


# Define exit key sequence.  For definition of modifier key strings see:
# http://www.psychopy.org/api/iohub/device/keyboard.html#keyboard-events
exit_detector = ExitDetector("q", ["lctrl", "rctrl"])

# Instantiate the shower class which presents specified stimuli from the bundle and records results
shower = ShowMaker(stim_bundle, exit_detector)



# "Clock.Information"       : dummy constant column
output_record = mid_scanner_record.MidScannerRecord(stim_bundle.data_dir_path, operator_table['file_name'])

# Create the data output spreadsheet and set some column values

# "ExperimentName"       : dummy constant but dependent on scanner type setting
experiment_name = version_keeper.experiment_name();
output_record.add_constant_column("ExperimentName", experiment_name )

# TODO: TODO: revise this to use operator inputs instead.  See comments with operator input methods.
output_record.add_constant_column("Subject", 1)
output_record.add_constant_column("Session", operator_table["session_number"])

# TODO: Unify this with the specification for allowed input keys for the probe. And figure out what 12 is (ascii?).
output_record.add_constant_column("Allowed", 12)

output_record.add_constant_column("DataFile.Basename", operator_table['file_name_without_extension'])

# Get the display frame rate and put it in the output table
framerate_hz = shower.get_framerate_hz()
output_record.add_constant_column("Display.RefreshRate", round(framerate_hz, 3))

output_record.add_constant_column("Group", operator_table['session_number'])
output_record.add_constant_column("Handedness", operator_table['handedness'])
output_record.add_constant_column("NARGUID", operator_table['subject_id'])
# TODO: Verify that this shoudl be the PracticeRT loaded from the dialog.
output_record.add_constant_column("PracticeRT", operator_table['average_rt'])
output_record.add_constant_column("RandomSeed", rand_gen.seed)
# "RuntimeCapabilities" is a dummy constant column
# "RuntimeVersion"          : dummy constant column
# "RuntimeVersionExpected"  : dummy constant column
session_date, utc_date_time, session_time = formatted_date_time()
output_record.add_constant_column("SessionDate", session_date)
output_record.add_constant_column("SessionStartDateTimeUtc", utc_date_time)
output_record.add_constant_column("SessionTime", session_time)
# "StudioVersion"           : dummy constant column
output_record.add_constant_column("TrialOrder", operator_table['trial_order_version'])
output_record.add_constant_column("triggercode", version_keeper.trigger_code())


# Open the stimulus window, fire up the IOHub engine to read key presses
screen_num = shower.setup()

# Find rt, earnings and run_num parameters from operater inputs and cache files
rt, earnings_dollars, run_num_start = find_rt_earnings_run_num(operator_table, stim_bundle)

# init probe_duration variable from rt value either loaded from cache file or input from operator.
probe_duration_secs = msecs_to_secs(rt)

# mark start time for timers which generates values for output columns:
#  - Probe.OnsetDelay
#  - Probe.OnsetTime
mark_start_time()
#  - Probe.OnsetToOnsetTime

# track of the real count of the current block.
real_block_identifier = 0;

# column had
period_list_sample_column = 0;

try:

    for block_index in range(run_num_start - 1, 2):     # This seems opaque and overcomplicated, check or rethink it.

        #TODO: Verify table column header values are correct for E-Prime output table which starts at run_num_start = 2
        # The current values were inferred from a table which started at 1.

        # Match eponymous E-Prime variable state value
        block_num = block_index + 1

        # Increment our general-purpose block identifier (without funky e-prime numbering policy).
        real_block_identifier += 1

        # Fetch the current block table.  If this is #2 numbered session then we start with the second block table
        block_table = block_tables[block_index]

        # E-Prime name: TitlePage
        shower.show("MID_Instructions", None, "SPACE_KEY")

        # This value fills in the "trial" column and is otherwise useless.
        trial_column = 1

        # Add the first of two header rows between 50-trial blocks
        output_record.add_new_row()
        # Write cells which are always NULL for both of a paired block header rows
        output_record.add_cell_value_to_columns(mid_scanner_record.inter_test_loop_nulls, "NULL")
        # Write cells which are always NULL for only the first block header rows
        output_record.add_cell_value_to_columns(mid_scanner_record.inter_test_loop_first_nulls, "NULL")
        # Write cell values which are non-null for the first block header row.
        output_record.add_cell_value_to_row("Trial", trial_column);
        #TODO: Figure out what this is and fill it in.
        #output_record.add_cell_value_to_row("GetReady.RTTime", );          # What is this?
        output_record.add_cell_value_to_row("Procedure[Trial]", "WaitScreen");
        output_record.add_cell_value_to_row("Running[Trial]", version_keeper.running_trial_header_cell_value());
        #TODO: Fetch column names contaning "GE" from our abcd_versions module to generalize on scanners.
        output_record.add_cell_value_to_row("Waiting4ScannerGE", 1);
        output_record.add_cell_value_to_row("Waiting4ScannerGE.Cycle", real_block_identifier);
        output_record.add_cell_value_to_row("Waiting4ScannerGE.Sample", real_block_identifier);
        # Note: At this point of execution the remaining unfilled block header cells for the first of paired block
        # header rows are constant column cells, either dummy or derived constants.


        # Wait for the scanner.  We use the space bar as a proxy for the scanner start sequence.
        num_start_sequences = scanner_waiting_table.cell_value("Weight", 1)
        # E-Prime name GetReady
        # TODO: Conditionally use the actual scanner start sequence here and add a degugging switch somewhere
        shower.show("GetReady", None, "SPACE_KEY")

        # increment trial column value (to two) for second line(of two) of block header
        trial_column += 1

        # This value fills in the "PeriodList.Sample" column and is otherwise useless
        period_list_sample_column += 1;

        # Add the second of two header rows between 50-trial blocks
        output_record.add_new_row()
        # Write cells which are always NULL for both of a paired block header rows
        output_record.add_cell_value_to_columns(mid_scanner_record.inter_test_loop_nulls, "NULL")
        # Write cells which are always NULL for only the second paired block header row
        output_record.add_cell_value_to_columns(mid_scanner_record.inter_test_loop_second_nulls, "NULL")
        # Write cell values which are non-null for the first block header row.
        #TODO: fill in values for all of these
        output_record.add_cell_value_to_row("Trial", trial_column)
        output_record.add_cell_value_to_row("PeriodList", 1)
        output_record.add_cell_value_to_row("PeriodList.Cycle", real_block_identifier)
        output_record.add_cell_value_to_row("PeriodList.Sample", period_list_sample_column)
        # output_record.add_cell_value_to_row("PrepTime.Duration", )            # ?? Look at E-Prime source ??
        # output_record.add_cell_value_to_row("PrepTime.DurationError", )       # ?? Look at E-Prime source ??
        # output_record.add_cell_value_to_row("PrepTime.FinishTime", )          # ?? Look at E-Prime source ??
        # output_record.add_cell_value_to_row("PrepTime.OffsetDelay", )         # ?? Look at E-Prime source ??
        # output_record.add_cell_value_to_row("PrepTime.OffsetTime", )          # ?? Look at E-Prime source ??
        # output_record.add_cell_value_to_row("PrepTime.OnsetDelay", )          # ?? Look at E-Prime source ??
        # output_record.add_cell_value_to_row("PrepTime.OnsetToOnsetTime", )    # ?? Look at E-Prime source ??
        # output_record.add_cell_value_to_row("PrepTime.StartTime", )           # ?? Look at E-Prime source ??
        output_record.add_cell_value_to_row("Procedure[Trial]", "PrepProc")
        output_record.add_cell_value_to_row("Running[Trial]", "PeriodList")


        # Note: At this point of execution the remaining unfilled block header cells for the second of paired block
        # header rows are constant column cells, either dummy or derived constants.

        # E-Prime name PrepTime
        shower.show("PrepTime", 2.0)

        # E-Prime name: CalculateProbeDuration
        probe_calculator = ProbeCalculator(probe_duration_secs)

        # Increment trial column value, which remains constant at 3 for both blocks
        trial_column += 1

        # Increment the "PeriodList.Sample" again. It stepped up at entry into block headers and entry into data here.
        period_list_sample_column += 1;

        # E-Prime name: RunProc
        for run_index in range(0, block_table.num_rows):

            # E-Prime name: Cue
            cue_file_name = block_table.cell_value("Cue", run_index + 1)
            stim_record_probe = shower.show_file(cue_file_name, 2.0)

            # E-Prime name: Anticipation
            # TODO: Make sure that we do not need to check for bogus keydowns here also.
            anticipation_duration_secs = msecs_to_secs(block_table.cell_value("AnticipationDuration", run_index + 1))
            stim_record_anticipation = shower.show("Anticipation", anticipation_duration_secs, "SPACE_KEY", None, False)

            # E-Prime name: Probe
            probe_file_name = block_table.cell_value("Probe", run_index + 1)
            probe_duration_secs = probe_calculator.probe_duration_secs
            feedback_duration_secs = probe_calculator.feedback_duration_secs
            stim_record_probe = shower.show_file(probe_file_name, probe_duration_secs, "SPACE_KEY", None, False)

            # E-Prime name: TextDisplay1 (just an empty screen)
            shower.show("TextDisplay1", 0.050)

            # E-Prime name: OutcomeFileNames
            probe_pressed = stim_record_probe.was_key_pressed
            anticipation_pressed = stim_record_anticipation.was_key_pressed

            # print("anticipation_pressed: " + str(anticipation_pressed))

            condition_name = block_table.cell_value("Condition", run_index + 1)
            response_ok, message_check, message, money = find_outcomes(anticipation_pressed, probe_pressed,
                                                                       condition_name)
            # E-Prime name: CalculateProbeDuration
            condition_name = block_table.cell_value("Condition", run_index + 1)
            response_ok = stim_record_probe.was_key_pressed

            # print("probe_pressed: " + str(response_ok))
            # print("")

            reaction_time_secs = stim_record_probe.key_down_exit_secs
            probe_calculator.add_probe(condition_name, response_ok, reaction_time_secs, money)

            # E-Prime name: Feedback
            text_subs_feedback = {"ResponseCheck" : message_check, "Result": message}
            shower.show("Feedback", feedback_duration_secs, [], text_subs_feedback)

            # Write rows for this trial
            output_record.add_new_row()
            output_record.add_cell_value_to_row("Block", block_num)
            output_record.add_cell_value_to_row("BlockList", block_num)
            output_record.add_cell_value_to_row("BlockList.Cycle", 1)
            output_record.add_cell_value_to_row("BlockList.Sample", block_num)
            block_title = block_list_table.cell_value("BlockTitle", block_num)
            output_record.add_cell_value_to_row("BlockTitle", block_title)
            

        # E-Prime name: EndFix
        shower.show("EndFix", 5.0)

        # E-Prime name: outputVars
        rt_msecs = secs_to_msecs(probe_duration_secs)
        money_total = probe_calculator.money_total
        should_quit = write_rt_earnings(operator_table, stim_bundle, block_num, rt_msecs, money_total)

        # TODO: conditionally break the loop on should_quit?

    # E-Prime name: DisplayMoney, Goodbye
    money_text_table = display_money_table(money_total)
    shower.show("DisplayMoney", None, "SPACE_KEY", money_text_table)

except UserExitRequest:
    shower.show_text("Exit command detected.  Press space bar to exit", None, "SPACE_KEY")

else:

    pass


finally:


    # Store the output spreadsheet
    # If the data is incomplete because we exited early then the "NewRT" and "IntNewRT" columns will not be present.
    output_record.save()
    print("output record saved.")

    # Close the stimulus window, shutdown the IOHUb engine used to read key presses.
    shower.shutdown()














