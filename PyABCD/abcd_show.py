# abcd_show.py
#
# Contains stuff used to present images and collect button responses from subject
#
# Notes:
#
# How E-Prime records timing audit parameters
# https://support.pstnet.com/hc/en-us/articles/115012671007-GENERAL-Object-Execution-22853-
# https://support.pstnet.com/hc/en-us/articles/115012775087
# ---------
# OnsetTime:
# "OnsetTime is the time immediately after the vertical refresh occurs and the draw command begins to execute."
#
# Timestamp (in milliseconds from the start of the experiment) when the stimulus presentation actually began.
# ---------
# OnsetToOnset:
# "However, E-Prime provides an easy way to obtain a close approximation to how long a stimulus appeared on screen.
# The OnsetToOnset time, which indicates how much time elapsed from the Onset of the current object to the onset time
# of the next object, can be logged in the data file by utilizing the TimeAudit feature"
#
# "Difference in milliseconds between the timestamp for the next object's OnsetTime and this object's OnsetTime"
# ---------
# OnsetDelay:
# "OnsetDelay and TargetOnsetTime: OnsetDelay is the difference between the TargetOnsetTime and the OnsetTime. The
# TargetOnsetTime is a timestamp calculated internally by E-Prime at the conclusion of the prior object."
#
# Difference in milliseconds between the actual onset time and the expected or "target" onset time. The "target"
# onset time is calculated internally by E-Prime as it prepares the object to be presented/processed.
# ---------
# DurationError:
# Difference in milliseconds between the actual duration and intended duration before the command ended. If the event
# is terminated by a response, a value of - 99999 will appear in the column (i.e., since the duration error cannot be
# computed in that sutation). Using (same as duration) for PreRelease makes this value obsolete.


from psychopy import visual, core, monitors, iohub
from abcd_window import *
from stim_bundle import *
from abcd_stimulus import *



#TODO: Detect the ePrime cancel sequence wich is probably metakeys in IOHub
#TODO: Document that modifier keys are ignored
#TODO: Instrument timing loop to find out what is taking time there
#TODO: Look for timing loop misses
#TODO: Raise priorit
#TODO: Check for other applications running and shut them down
#TODO: Make sure synchronized flips are turned on
#TODO: Write a test suite to accompany ABCD

# TODO: Set this dynamically at 2x the frame rate + foo.
POLLING_LOOP_FREQUENCY_HZ = 200.0

polling_loop_period_secs = 1/POLLING_LOOP_FREQUENCY_HZ

# "C:\Program Files (x86)\PsychoPy2\python.exe"
#
# from psychopy import visual
# from psychopy import event
#
# w = visual.Window(screen=0)
# ks=event.waitKeys()
# print(ks)

experiment_start_secs = None

def mark_start_time():
    global experiment_start_secs
    experiment_start_secs = core.getTime()


# functions for discriminating between keyups and keydowns.
def is_keypress(event):
    # String comparison is a workaround for Python claiming that psychopy.iohub.devices.KeyboardPressEventNT does not
    # exist.  We would otherwise use isinstance or issubclass here.
    return str(type(event)) == "<class 'psychopy.iohub.devices.KeyboardPressEventNT'>"

def is_keyrelease(event):
    # String comparison is a workaround for Python claiming that psychopy.iohub.devices.KeyboardPressEventNT does not
    # exist.  We would otherwise use isinstance or issubclass here.
    return str(type(event)) == "<class 'psychopy.iohub.devices.KeyboardReleaseEventNT'>"


# list of key names
key_names_table = {}


def add_key_name(name, character):
    key_names_table[name] = character
    #globals()[name] = character


def key_name_for_char(character):
    name_matches = [key_name for key_name in key_names_table if key_names_table[key_name] == character]
    if name_matches:
        return name_matches[0]
    else:
        return character


def key_char_for_name(name):
    if name in key_names_table:
        return key_names_table[name]
    else:
        return name


add_key_name("SPACE_KEY", " ")


def get_keydown(keyboard, filter_in_keys):
    for event in keyboard.getEvents():
        if event.key in filter_in_keys:
            if is_keypress(event):
                return event.key, event.time
    return None


class StimRecord:
    """Retains data from a single Presenter trial

    An experiment's Presenter instance generates one StimRecord instance per trial to retain a record of the image
    presented, its sequence and the subject response.

    Attributes:
        stim_index (int): Zero-indexed value incremented for each presentation
        image_name (str): Name of the image file presented
        timeout (float): The time limit after stimulus onset that trial ends if a filtered key was not pressed.
        filter_in_keys (list of strs): Keys which were not ignored
        gotten_key (str): The first keypress in filter_in_keys recorded
        stim_afterflip_secs (float): Timestamp of when the flip displaying the stimulus returns.
        clear_afterflip_secs (float): Image offset time in secs
        key_secs (float): Keypress time in secs

    """

    def __init__(self, stim_index, stimulus_name, timeout_secs, filter_in_keys, stim_afterflip_secs,
                 clear_afterflip_secs, did_timeout, key_downs):
        """Init an instance of StimRecord with arguments for all properties except those derived by accessors.

        Args:
            stim_index (int): Zero-indexed value incremented for each presentation
            stimulus_name (str): Name of the image or text file presented
            timeout (float): The time limit after stimulus onset that trial ends if a filtered key was not pressed.
            filter_in_keys (list of strs): Keys which were not ignored
            gotten_key (str): The first keypress in filter_in_keys recorded
            stim_afterflip_secs (float): Image onset time in secs
            clear_afterflip_secs (float): Timestamp of when the flip clearing the stimulus returns.
            key_secs (float): Keypress time in secs

        """
        self.stim_index = stim_index
        self.stimulus_name = stimulus_name
        self.timeout_secs = timeout_secs
        self.filter_in_keys = filter_in_keys
        self.stim_afterflip_secs = stim_afterflip_secs
        self.clear_afterflip_secs = clear_afterflip_secs
        self.did_timeout = did_timeout
        self.key_downs = key_downs
        self.blank_rgb = [127, 127, 127]

    @property
    def stimulus_duration_secs(self):
        return self.clear_afterflip_secs - self.stim_afterflip_secs

    @property
    def first_keydown_delay_secs(self):
        """float: delay in seconds between stimulus presentation and keypress or None iff timeout."""
        if self.key_downs:
            return self.key_downs[0][1] - self.stim_afterflip_secs # It's full of nones', only store keydowns when there is one
        else:
            return None

    @property
    def is_timeout_enabled(self):
        return self.timeout_secs is not None

    @property
    def was_key_pressed(self):
        return bool(self.key_downs)

    @property
    def onset_time_msecs(self):
        return secs_to_msecs(self.stim_afterflip_secs - experiment_start_secs)

    @property
    def onset_to_onset_time_msecs(self):
        return secs_to_msecs(self.clear_afterflip_secs - self.stim_afterflip_secs)

    def duration_error_msecs(self, nominal_duration_secs):
        return secs_to_msecs(self.clear_afterflip_secs - self.stim_afterflip_secs - nominal_duration_secs)

    def onset_delay_msecs(self, previous_stim_record):
        return secs_to_msecs(self.stim_afterflip_secs - previous_stim_record.clear_afterflip_secs)

    def __str__(self):
        txt = ""
        txt += "stim_index: %d\n" % self.stim_index
        txt += "stimulus_name: %s\n" % self.stimulus_name
        txt += "timeout_secs: %s\n" % str(self.timeout_secs)  # convert to string for case None
        txt += "filter_in_keys: %s\n" % str([key_name_for_char(key_char) for key_char in self.filter_in_keys])
        txt += "stim_afterflip_secs: %f\n" % self.stim_afterflip_secs
        txt += "clear_afterflip_secs: %f\n" % self.clear_afterflip_secs
        txt += "did_timeout %s\n" % self.did_timeout
        txt += "blank_rgb: %s\n" % str(self.blank_rgb)
        txt += "stimulus_duration_secs: %f\n" % self.stimulus_duration_secs
        txt += "first_keydown_delay_secs: %s\n" % self.first_keydown_delay_secs
        return txt


class Show:

    stimulus_counter = None
    io = None
    keyboard = None

    @classmethod
    def reset_stimulus_counter(cls):
        cls.stimulus_counter = None

    @classmethod
    def new_stimulus_index(cls):
        if cls.stimulus_counter is None:
            cls.stimulus_counter = 0
        else:
            cls.stimulus_counter += 1
        return cls.stimulus_counter

    @classmethod
    def setup(cls):
        if cls.io is not None:
            cls.io.quit()
        cls.io = iohub.launchHubServer()
        cls.keyboard = cls.io.devices.keyboard

    @classmethod
    def shutdown(cls):
        if cls.io is not None:
            cls.io.quit()
        cls.io = None
        cls.keyboard = None

    def __init__(self, window, stim_bundle, stimulus_name, timeout_secs, filter_in_key_names, text_subs=None,
                 exit_on_key=True):
        # TODO: It would be better to not instantiate self.image_stim here to make command-line testing easier..
        # TODO:     ..It requires and open window.
        self.window = window
        self.stim_bundle = stim_bundle
        self.stimulus_name = stimulus_name
        self.timeout_secs = timeout_secs
        self.text_subs = text_subs
        self.exit_on_key = exit_on_key
        if isinstance(filter_in_key_names, str):
            filter_in_key_names = [filter_in_key_names]
        self.filter_in_keys = [key_char_for_name(name) for name in filter_in_key_names]
        self.records = None
        #self.path_to_image = self.stim_bundle.image_path_for_name(self.image_name)
        #self.image_stim = visual.ImageStim(self.window, image=self.path_to_image, units='pix')
        self.stimulus = Stimulus(self.stim_bundle, self.window, self.stimulus_name, self.text_subs)

    def is_timeout_mode(self):
        return self.timeout_secs is not None

    def show(self):
        key_down_exit = False
        timeout_flag = False
        self.io.clearEvents()
        self.stimulus.draw_flip()
        stim_afterflip_secs = core.getTime()
        key_downs = []
        while not key_down_exit and not timeout_flag:
            key_down = get_keydown(self.keyboard, self.filter_in_keys)
            if(key_down):
                key_downs.append(key_down)
            key_down_exit = key_down and self.exit_on_key
            elapsed_time_secs = core.getTime() - stim_afterflip_secs
            timeout_flag = self.is_timeout_mode() and elapsed_time_secs > self.timeout_secs
            if not key_down_exit and not timeout_flag:
                core.wait(polling_loop_period_secs)
        #TODO: Draw a blank screen or the next frame here?
        self.stimulus.clear_flip()
        clear_afterflip_secs = core.getTime()
        stim_index = self.__class__.new_stimulus_index()
        stim_record = StimRecord(stim_index, self.stimulus_name, self.timeout_secs, self.filter_in_keys,
                                 stim_afterflip_secs, clear_afterflip_secs, timeout_flag, key_downs)
        return stim_record


class ShowMaker:
    """A convenience wrapper for the Show class which retains some arguments allowing abbreviated functions calls."""

    def __init__(self, stim_bundle):
        self.window = None
        self.stim_bundle = stim_bundle
        self.stim_records = []

    def show(self, stimulus_name, timeout_secs, filter_in_key_names=[], text_subs=None, exit_on_key=True):
        shower = Show(self.window, self.stim_bundle, stimulus_name, timeout_secs, filter_in_key_names, text_subs,
                      exit_on_key)
        result_record = shower.show()
        self.stim_records.append(result_record)
        return result_record

    def show_file(self, file_name, timeout_secs, filter_in_key_names=[], text_subs=None, exit_on_key=True):
        stimulus_name = os.path.splitext(file_name)[0]
        result_record = self.show(stimulus_name, timeout_secs, filter_in_key_names, text_subs, exit_on_key)
        return result_record

    def setup(self):
        if self.window is None:
            self.window = open_stimulus_window()
            Show.setup()
            self.stim_records = []
            return self.window.screen
        else:
            print("Error: Attempt to setup the ShowMaker when it is already setup.")
            sys.exit()

    def get_framerate_hz(self):
        if self.window:
            rate_hz = self.window.getActualFrameRate()
            return rate_hz
        return None

    def shutdown(self):
        if self.window is None:
            print("Error: Attempt to shutdown the ShowMaker when it is not setup.")
            sys.exit()
        else:
            close_stimulus_window()
            Show.shutdown()

    def print_records(self):
        for record in self.stim_records:
            print("")
            print(record)




















