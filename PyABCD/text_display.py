
import json
import stim_bundle

class TextDisplay:

        def __init__(self, stim_bundle, text_display_name):
            path_to_text_display_file = stim_bundle.text_display_path_for_name(text_display_name)
            path_to_text_json_file = stim_bundle.text_json_path_for_name(text_display_name)


