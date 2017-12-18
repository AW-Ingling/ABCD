# abcd_show.py
#
# Contains stuff used to present images and collecte button responses from subject

from psychopy import visual, core, monitors, iohub


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



def get_key(keyboard, filter_in_keys):
    for event in keyboard.getEvents():
        if event.key in filter_in_keys:
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

    def __init__(self, stim_index, image_name, timeout_secs, filter_in_keys, gotten_key, start_secs, stop_secs, key_secs):
        """Init an instance of StimRecord with arguments for all properties except those derived by accessors.

        Args:
            stim_index (int): Zero-indexed value incremented for each presentation
            image_name (str): Name of the image file presented
            timeout (float): The time limit after stimulus onset that trial ends if a filtered key was not pressed.
            filter_in_keys (list of strs): Keys which were not ignored
            gotten_key (str): The first keypress in filter_in_keys recorded
            start_secs (float): Image onset time in secs
            stop_secs (float): Image offset time in secs
            key_secs (float): Keypress time in secs

        """
        self.stim_index = stim_index
        self.image_name = image_name
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
    def response_secs(self):
        """float: delay in seconds between stimulus presentation and keypress or None iff timeout."""
        if self.key_secs:
            return self.key_secs - self.start_secs
        else:
            return None

    def __str__(self):
        txt = ""
        txt += "stim_index: %d\n" % self.stim_index
        txt += "image_name: %s\n" % self.image_name
        txt += "timeout_secs: %s\n" % str(self.timeout_secs)
        txt += "filter_in_keys: %s\n" % str(self.filter_in_keys)
        txt += "gotten_key: %s\n" % self.gotten_key
        txt += "start_secs: %d\n" % self.start_secs
        txt += "stop_secs: %d\n" % self.stop_secs
        txt += "key_secs: %d\n" % self.key_secs
        txt += "blank_rgb: %s\n" % str(self.blank_rgb)
        txt += "stimulus_duration_secs: %d\n" % self.stimulus_duration_secs
        txt += "response_secs: %d\n" % self.response_secs
        return txt

class Presenter:

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

    def __init__(self, window, stim_bundle, image_name, timeout_secs, filter_in_keys):
        self.window = window
        self.stim_bundle = stim_bundle
        self.image_name = image_name
        self.timeout_secs = timeout_secs
        self.filter_in_keys = filter_in_keys
        self.records = None
        self.path_to_image = self.stim_bundle.image_path_for_name(self.image_name)
        self.image_stim = visual.ImageStim(self.window, image=self.path_to_image, units='pix')

    def show_image(self):
        keypress = False
        timeout_flag = False
        self.io.clearEvents()
        self.image_stim.draw()
        self.window.flip()
        start_secs = core.getTime()
        while not keypress or timeout_flag:
            keypress = get_key(self.keyboard, self.filter_in_keys)
            end_time_secs = core.getTime()
            elapsed_time_secs = end_time_secs - start_secs
            timeout_flag = self.timeout_secs and elapsed_time_secs > self.timeout_secs
            if not timeout_flag or keypress:
                core.wait(polling_loop_period_secs)
        #TODO: Draw a blank screen or the next frame here?
        stop_secs= core.getTime()
        stim_index = self.__class__.new_stimulus_index()
        stim_record = StimRecord(stim_index, self.image_name, self.timeout_secs, self.filter_in_keys, keypress[0],
                                 start_secs, stop_secs, keypress[1])
        return stim_record











