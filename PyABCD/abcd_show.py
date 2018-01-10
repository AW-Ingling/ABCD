# abcd_show.py
#
# Contains stuff used to present images and collecte button responses from subject

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

POLLING_LOOP_FREQUENCY_HZ = 100.0

polling_loop_period_secs = 1/POLLING_LOOP_FREQUENCY_HZ

# "C:\Program Files (x86)\PsychoPy2\python.exe"
#
# from psychopy import visual
# from psychopy import event
#
# w = visual.Window(screen=0)
# ks=event.waitKeys()
# print(ks)


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
        start_secs (float): Image onset time in secs
        stop_secs (float): Image offset time in secs
        key_secs (float): Keypress time in secs

    """

    def __init__(self, stim_index, stimulus_name, timeout_secs, filter_in_keys, gotten_key, start_secs, stop_secs, key_secs):
        """Init an instance of StimRecord with arguments for all properties except those derived by accessors.

        Args:
            stim_index (int): Zero-indexed value incremented for each presentation
            stimulus_name (str): Name of the image or text file presented
            timeout (float): The time limit after stimulus onset that trial ends if a filtered key was not pressed.
            filter_in_keys (list of strs): Keys which were not ignored
            gotten_key (str): The first keypress in filter_in_keys recorded
            start_secs (float): Image onset time in secs
            stop_secs (float): Image offset time in secs
            key_secs (float): Keypress time in secs

        """
        self.stim_index = stim_index
        self.stimulus_name = stimulus_name
        self.timeout_secs = timeout_secs
        self.filter_in_keys = filter_in_keys
        self.gotten_key = gotten_key
        self.start_secs = start_secs
        self.stop_secs = stop_secs
        self.key_secs = key_secs
        self.blank_rgb = [127, 127, 127]

    @property
    def stimulus_duration_secs(self):
        return self.stop_secs - self.start_secs

    @property
    def keypress_delay_secs(self):
        """float: delay in seconds between stimulus presentation and keypress or None iff timeout."""
        if self.key_secs:
            return self.key_secs - self.start_secs
        else:
            return None

    @property
    def was_keypress_before_timeout(self):
        return self.key_down_key is not None and self.key_down_time is not None

    def __str__(self):
        txt = ""
        txt += "stim_index: %d\n" % self.stim_index
        txt += "stimulus_name: %s\n" % self.stimulus_name
        txt += "timeout_secs: %s\n" % str(self.timeout_secs)  # convert to string for case None
        txt += "filter_in_keys: %s\n" % str([key_name_for_char(key_char) for key_char in self.filter_in_keys])
        txt += "gotten_key: %s\n" % key_name_for_char(self.gotten_key)
        txt += "start_secs: %f\n" % self.start_secs
        txt += "stop_secs: %f\n" % self.stop_secs
        txt += "key_secs: %s\n" % str(self.key_secs)
        txt += "blank_rgb: %s\n" % str(self.blank_rgb)
        txt += "stimulus_duration_secs: %f\n" % self.stimulus_duration_secs
        txt += "keypress_delay_secs: %f\n" % self.keypress_delay_secs
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

    def __init__(self, window, stim_bundle, stimulus_name, timeout_secs, filter_in_key_names, text_subs=None):
        # TODO: It would be better to not instantiate self.image_stim here to make command-line testing easier..
        # TODO:     ..It requires and open window.
        self.window = window
        self.stim_bundle = stim_bundle
        self.stimulus_name = stimulus_name
        self.timeout_secs = timeout_secs
        self.text_subs = text_subs
        if isinstance(filter_in_key_names, str):
            filter_in_key_names = [filter_in_key_names]
        self.filter_in_keys = [key_char_for_name(name) for name in filter_in_key_names]
        self.records = None
        #self.path_to_image = self.stim_bundle.image_path_for_name(self.image_name)
        #self.image_stim = visual.ImageStim(self.window, image=self.path_to_image, units='pix')
        self.stimulus = Stimulus(self.stim_bundle, self.window, self.stimulus_name, self.text_subs)

    def show(self):
        key_down = False
        timeout_flag = False
        self.io.clearEvents()
        self.stimulus.draw_flip()
        #self.image_stim.draw()
        #self.window.flip()
        start_secs = core.getTime()
        while not key_down and not timeout_flag:
            key_down = get_keydown(self.keyboard, self.filter_in_keys)
            end_time_secs = core.getTime()
            elapsed_time_secs = end_time_secs - start_secs
            timeout_flag = self.timeout_secs and elapsed_time_secs > self.timeout_secs
            if not timeout_flag or key_down:
                core.wait(polling_loop_period_secs)
        #TODO: Draw a blank screen or the next frame here?
        stop_secs= core.getTime()
        stim_index = self.__class__.new_stimulus_index()
        if timeout_flag:
            key_down_key = None
            key_down_time = None
        else:
            key_down_key = key_down[0]
            key_down_time = key_down[1]
        stim_record = StimRecord(stim_index, self.stimulus_name, self.timeout_secs, self.filter_in_keys, key_down_key,
                                 start_secs, stop_secs, key_down_time)
        return stim_record


class ShowMaker:
    """A convenience wrapper for the Show class which retains some arguments allowing abbreviated functions calls."""

    def __init__(self, stim_bundle):
        self.window = None
        self.stim_bundle = stim_bundle
        self.stim_records = []

    def show(self, stimulus_name, timeout_secs, filter_in_key_names=[], text_subs=None):
        shower = Show(self.window, self.stim_bundle, stimulus_name, timeout_secs, filter_in_key_names, text_subs)
        result_record = shower.show()
        self.stim_records.append(result_record)
        return result_record

    def show_file(self, file_name, timeout_secs, filter_in_key_names=[], text_subs=None):
        stimulus_name = os.path.splitext(file_name)[0]
        result_record = self.show(stimulus_name, timeout_secs, filter_in_key_names, text_subs)
        return result_record

    def setup(self):
        if self.window is None:
            self.window = open_stimulus_window()
            Show.setup()
            self.stim_records = []
        else:
            print("Error: Attempt to setup the ShowMaker when it is already setup.")
            sys.exit()

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




















