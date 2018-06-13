

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

# Create the data output spreadsheet and set some fields
output_record = mid_scanner_record.MidScannerRecord(stim_bundle.data_dir_path, operator_table['file_name'])
output_record.add_constant_column("DataFile.Basename", operator_table['file_name_without_extension'])
output_record.add_constant_column("Group", operator_table['session_number'])
output_record.add_constant_column("Handedness", operator_table['handedness'])
output_record.add_constant_column("NARGUID", operator_table['subject_id'])
session_date, utc_date_time, session_time = formatted_date_time()
output_record.add_constant_column("SessionDate", session_date)
output_record.add_constant_column("SessionStartDateTimeUtc", utc_date_time)
output_record.add_constant_column("SessionTime", session_time)

# Open the stimulus window, fire up the IOHub engine to read key presses
screen_num = shower.setup()

# Get the display frame rate and put it in the output table
framerate_hz = shower.get_framerate_hz()
output_record.add_constant_column("Display.RefreshRate", round(framerate_hz, 3))
output_record.add_constant_column("RandomSeed", rand_gen.seed)

# Find rt, earnings and run_num parameters from operater inputs and cache files
rt, earnings_dollars, run_num_start = find_rt_earnings_run_num(operator_table, stim_bundle)

# init probe_duration variable from rt value either loaded from cache file or input from operator.
probe_duration_secs = msecs_to_secs(rt)

# mark start time for timers which generates values for output columns:
#  - Probe.OnsetDelay
#  - Probe.OnsetTime
#  - Probe.OnsetToOnsetTime
mark_start_time()

try:

    for run_num_index in range(run_num_start - 1, 2):

        # Match eponymous E-Prime variable state value
        run_num = run_num_index + 1

        # Fetch the current block table.  If this is #2 numbered session then we start with the second block table
        block_table = block_tables[run_num_index]

        # E-Prime name: TitlePage
        shower.show("MID_Instructions", None, "SPACE_KEY")

        # Wait for the scanner.  We use the space bar as a proxy for the scanner start sequence.
        num_start_sequences = scanner_waiting_table.cell_value("Weight", 1)
        # E-Prime name GetReady
        # TODO: Use the actual scanner start sequence here
        shower.show("GetReady", None, "SPACE_KEY")

        # E-Prime name PrepTime
        shower.show("PrepTime", 2.0)

        # E-Prime name: CalculateProbeDuration
        probe_calculator = ProbeCalculator(probe_duration_secs)

        # E-Prime name: RunProc
        for run_index in range(0, block_table.num_rows):

            # E-Prime name: Cue
            cue_file_name = block_table.cell_value("Cue", run_index + 1)
            stim_record_probe = shower.show_file(cue_file_name, 2.0)

            # E-Prime name: Anticipation
            anticipation_duration_secs = msecs_to_secs(block_table.cell_value("AnticipationDuration", run_index + 1))
            stim_record_anticipation = shower.show("Anticipation", anticipation_duration_secs)

            # E-Prime name: Probe
            probe_file_name = block_table.cell_value("Probe", run_index + 1)
            probe_duration_secs = probe_calculator.probe_duration_secs
            feedback_duration_secs = probe_calculator.feedback_duration_secs
            stim_record_probe = shower.show_file(probe_file_name, probe_duration_secs, "SPACE_KEY")

            # E-Prime name: TextDisplay1 (just an empty screen)
            shower.show("TextDisplay1", 0.050)

            # E-Prime name: CalculateProbeDuration
            condition_name = block_table.cell_value("Condition", run_index + 1)
            response_ok = stim_record_probe.was_key_pressed
            reaction_time_secs = stim_record_probe.key_down_exit_secs
            probe_duration_secs.add_probe(condition_name, response_ok, reaction_time_secs, money)

            # E-Prime name: OutcomeFileNames
            probe_pressed = stim_record_probe.was_key_pressed
            anticipation_pressed =  stim_record_anticipation.was_key_pressed
            condition_name = block_table.cell_value("Condition", run_index + 1)
            response_ok, message_check, message, money = find_outcomes(anticipation_pressed, probe_pressed, condition_name)

            # E-Prime name: Feedback
            text_subs_feedback = {"ResponseCheck" : message_check, "Result": message}
            shower.show("Feedback", feedback_duration_secs, [], text_subs_feedback)

        # E-Prime name: EndFix
        shower.show("EndFix", 5.0)

        # E-Prime name: outputVars
        rt_msecs = secs_to_msecs(probe_duration_secs)
        money_total = probe_calculator.money_total
        should_quit = write_rt_earnings(operator_table, stim_bundle, run_num, rt_msecs, money_total)

        # TODO: conditionally break the loop on should_quit?

    # E-Prime name: DisplayMoney, Goodbye
    money_text_table = display_money_table(money_total)
    shower.show("DisplayMoney", None, "SPACE_KEY", text_subs_feedback)

except UserExitRequest:
    shower.show_text("Exit command detected.  Press space bar to exit", None, "SPACE_KEY")

else:

    pass


finally:


    # Store the output spreadsheet
    # If the data is incomplete because we exited early then the "NewRT" and "IntNewRT" columns will not be present.
    output_record.save()

    # Close the stimulus window, shutdown the IOHUb engine used to read key presses.
    shower.shutdown()














