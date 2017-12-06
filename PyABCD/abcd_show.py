# abcd_show.py
#
# Contains stuff used to present images and collecte button responses from subject

from psychopy import visual, core, monitors, event


#TODO: Detect the ePrime cancel sequence
#TODO: Document that modifier keys are ignored

# "C:\Program Files (x86)\PsychoPy2\python.exe"
#
# from psychopy import visual
# from psychopy import event
#
# w = visual.Window(screen=0)
# ks=event.waitKeys()
# print(ks)

class StimRecord:

    def __init__(self, stim_index, image_name, filter_keys, gotten_keys):
        self.stim_index = stim_index
        self.image_name = image_name
        self.filter_keys = filter_keys
        self.gotten_keys = gotten_keys






class Presenter:

    def __init__(self, window, stim_bundle):
        self.window = window
        self.stim_bundle = stim_bundle
        self.image_stim = None
        self.records = {}

    def show_image_until_input(self, stim_index, image_name, filter_keys):
        path_to_image = self.stim_bundle.image_path_for_name(image_name)
        keypress = False
        event.clearEvents('keyboard')
        while not keypress:
            self.image_stim = visual.ImageStim(self.window, image=path_to_image)
            event.getKeys(keyList=None, timeStamped=True)



