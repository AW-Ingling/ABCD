import sys
import json
import stim_bundle

from psychopy import visual, core, monitors, iohub


class Stimulus:

    """Abstracts up image and text stimuli into a common class"""

    def __init__(self, stim_bundle, window, name):
        # retain arguments and init defaults
        self.window = window
        self.image_stim = None
        self.text_stim = None
        self.text = None
        self.layout = None
        self.path_to_image = None
        self.path_to_text_display_file = None
        self.path_to_text_json_file = None
        # conditionally instantiate image or text resources
        if stim_bundle.is_image_name(name):
            self.path_to_image = stim_bundle.image_path_for_name(name)
            self.image_stim = visual.ImageStim(window, image=self.path_to_image, units='pix')
        elif stim_bundle.is_text_display_name(name):
            self.path_to_text_display_file = stim_bundle.text_display_path_for_name(name)
            self.path_to_text_json_file = stim_bundle.text_json_path_for_name(name)
            with open(self.path_to_text_display_file, 'r') as text_file:
                self.text = text_file.read()
            with open(self.path_to_text_json_file, 'r') as layout_file:
                self.layout = json.load(layout_file)
            self.text_stim = visual.TextStim(window, text='Hello \n World')
        else:
            print("ERROR: %s is an unrecognized stimulus type, neither image nor text." % name)
            sys.exit()

    def draw_flip(self):
        # Conditionally draw either the image or text stimulus then buffer flip
        if self.image_stim:
            self.image_stim.draw()
        elif self.text_stim:
            self.text_stim.draw()
        self.window.flip()











