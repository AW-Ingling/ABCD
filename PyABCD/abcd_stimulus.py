import sys
import json
import stim_bundle
from abcd_text import *

from psychopy import visual, core, monitors, iohub


# TODO: Verify this converstion by comparing images
# TODO: Verify that aliasing matches original E-Prime stimulus
def points_to_pixels(points):
    pixels_per_inch = 96.0
    points_per_inch = 72.0
    size_pixels = points / points_per_inch * pixels_per_inch
    return size_pixels


class Stimulus:

    """Abstracts up image and text stimuli into a common class"""

    @classmethod
    def make_bundle_stimulus(cls, window, stim_bundle, name, text_subs=None):
        stimulus = Stimulus(window)
        stimulus.stim_bundle = stim_bundle
        stimulus.name = name
        stimulus.text_subs = text_subs
        stimulus.is_bundle_stimulus = True
        stimulus.setup_bundle_stimulus()
        return stimulus

    @classmethod
    def make_string_stimulus(cls, window, message, font_name="verdana", point_size=18):
        stimulus = Stimulus(window)
        stimulus.message = message
        stimulus.font_name = font_name
        stimulus.point_size = point_size
        stimulus.is_bundle_stimulus = False
        stimulus.setup_string_stimulus()
        return stimulus

#    def __init__(self, stim_bundle, window, name, text_subs=None):
    def __init__(self, window):
        # variables assigned by class method constructors
        self.window = window
        self.stim_bundle = None
        self.name = None
        self.text_subs = None
        self.is_bundle_stimulus = None
        self.message = None
        self.font_name = None
        self.point_size = None
        # init defaults
        self.image_stim = None
        self.text_block = None
        self.raw_text = None
        self.layout = None
        self.path_to_image = None
        self.path_to_text_display_file = None
        self.path_to_text_json_file = None

    def setup_bundle_stimulus(self):

        # conditionally instantiate image or text resources
        if self.stim_bundle.is_image_name(self.name):
            self.path_to_image = self.stim_bundle.image_path_for_name(self.name)
            self.image_stim = visual.ImageStim(self.window, image=self.path_to_image, units='pix')
        elif self.stim_bundle.is_text_display_name(self.name):
            self.path_to_text_display_file = self.stim_bundle.text_display_path_for_name(self.name)
            self.path_to_text_json_file = self.stim_bundle.text_json_path_for_name(self.name)
            with open(self.path_to_text_display_file, 'r') as text_file:
                self.raw_text = text_file.read()
            with open(self.path_to_text_json_file, 'r') as layout_file:
                self.layout = json.load(layout_file)
            self.text = self.raw_text
            if self.text_subs:
                for key in self.text_subs:
                    key_str = '[' + key + ']'
                    self.text = self.text.replace(key_str, self.text_subs[key])
            # self.text_stim = visual.TextStim(window,
            #                                  font=self.layout['font']['name'],
            #                                  bold=self.layout['font']['bold'],
            #                                  italic=self.layout['font']['italic'],
            #                                  alignHoriz=self.layout['general']['align_horizontal'],
            #                                  alignVert=self.layout['general']['align_vertical'],
            #                                  color=self.layout['general']['forecolor'],
            #                                  units='pix',
            #                                  height=points_to_pixels(self.layout['font']['point_size']),
            #                                  text=self.text)
            font_size_pixels = points_to_pixels(self.layout['font']['point_size'])
            self.text_block = TextBlock(self.window, self.text, self.layout['font']['name'], font_size_pixels)
            #TODO: Communicated all parameters in the json text format file to the TextBlock init.
            self.text_block.format()
            #TODO: Detect and warn if not all variables are used in either the text file or dictionary
        else:
            print("ERROR: %s is an unrecognized stimulus type, neither image nor text." % self.name)
            sys.exit()

    def setup_string_stimulus(self):
        font_size_pixels = points_to_pixels(self.point_size)
        self.text_block = TextBlock(self.window, self.message, self.font_name, font_size_pixels)
        self.text_block.format()

    def draw_flip(self):
        # Conditionally draw either the image or text stimulus then buffer flip
        if self.image_stim:
            self.image_stim.draw()
        elif self.text_block:
            self.text_block.draw()
        self.window.flip()


    def clear_flip(self):
        # Clear the window and flip
        self.window.clearBuffer()
        self.window.flip()















