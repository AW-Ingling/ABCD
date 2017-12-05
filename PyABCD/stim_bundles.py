# abcd_images.py
#
# Author: Allen W. Ingling
#

# REFERENCES
#
# Code snippet for initializing a class, not an instance
# https://stackoverflow.com/questions/6183704/how-to-initialize-classes-not-instances-in-python
#
# Code snippet for finding the path to a class
# https://stackoverflow.com/questions/697320/how-do-i-get-the-filepath-for-a-class-in-python

# NOTES
# To find path to file from instance:
# os.path.realpath(__file__)

import os
import sys
from abcd_helpers import *

class MetaStimBundle(type):
    def __init__(cls, name, bases, d):
        type.__init__(cls, name, bases, d)
        cls.init_class()


class StimBundle:

    __metaclass__ = MetaStimBundle

    image_sets_dir_name = u'ImageSets'
    original_image_dir_name = u'OriginalImages'
    captured_image_dir_name = u'CapturedImages'

    @classmethod
    def original_dir_path_from_bundle_path(cls, bundle_path):
        return os.path.join(bundle_path, cls.original_image_dir_name)

    @classmethod
    def captured_dir_path_from_bundle_path(cls, bundle_path):
        return os.path.join(bundle_path, cls.captured_image_dir_name)

    @classmethod
    def is_bundle(cls, path_to_bundle):
        return (os.path.isdir(path_to_bundle)
                and os.path.isdir(cls.original_dir_path_from_bundle_path(path_to_bundle))
                and os.path.isdir(cls.captured_dir_path_from_bundle_path(path_to_bundle)))

    @classmethod
    def init_class(cls):
        # derive the paths to the project component dirs from the path to this file.
        cls.scripts_dir_path = os.path.split(os.path.abspath(sys.modules[cls.__module__].__file__))[0]
        cls.project_dir_path = os.path.split(cls.scripts_dir_path)[0]
        cls.bundles_dir_path = os.path.join(cls.project_dir_path, cls.image_sets_dir_name)

    @classmethod
    def bundle_name_path_table(cls):
        if os.path.isdir(cls.bundles_dir_path):
            all_dir_names = os.listdir(cls.bundles_dir_path)
            all_dir_paths = [os.path.join(cls.bundles_dir_path, dir_name) for dir_name in all_dir_names]
            return {pair[0]:pair[1] for pair in zip(all_dir_names, all_dir_paths) if cls.is_bundle(pair[1])}
        else:
            return {}

    @classmethod
    def bundle_names(cls):
        name_path_table = cls.bundle_name_path_table()
        return name_path_table.keys()

    @staticmethod
    def image_table_from_path(image_dir_path):
        all_file_names = os.listdir(image_dir_path)
        image_file_names = [filename for filename in all_file_names if is_image_file(filename)]
        image_names = [os.path.splitext(filename)[0] for filename in image_file_names]
        image_names_caps = [name.upper() for name in image_names]
        duplicate_image_cap_names = find_duplicates(image_names_caps)
        if duplicate_image_cap_names:
            name_cap_table = {pair[0]:pair[1] for pair in zip(image_names_caps, image_names)}
            duplicate_names = [name_cap_table[cap_name] for cap_name in duplicate_image_cap_names]
            print("Error: Directory containts duplicate image file names, Exiting.")
            print("\tdirectory: %s." % image_dir_path)
            print("\tduplicates: %s." % str(duplicate_names))
            sys.exit()
            #TODO: Issue and error dialog here
            # TODO: Test that this duplicate detector stuff works
        image_file_paths = [os.path.join(image_dir_path, file_name) for file_name in image_file_names]
        image_path_table = {pair[0]: pair[1] for pair in zip(image_names, image_file_paths)}
        return image_path_table

    def __init__(self, bundle_name):
        # retain and derive some path names into the bundle
        self.bundle_name = bundle_name
        bundle_path_table = self.bundle_name_path_table()
        if not self.bundle_name in bundle_path_table:
            print("ERROR: Failed to find stimulus bundle with name: %s." % str(bundle_name))
            sys.exit()
            #TODO: Issue an error dialog here.
        self.bundle_path = bundle_path_table[bundle_name]
        self.original_images_path = self.original_dir_path_from_bundle_path(self.bundle_path)
        self.captured_images_path = self.captured_dir_path_from_bundle_path(self.bundle_path)
        # generate a table mapping from the image name to image file path.
        self.original_images_table = self.image_table_from_path(self.original_images_path)
        self.captured_images_table = self.image_table_from_path(self.captured_images_path)
        original_upper = [image_name.upper() for image_name in self.original_images_table.keys()]
        captured_upper = [image_name.upper() for image_name in self.captured_images_table.keys()]
        dupe_image_names = list(set(original_upper).intersection(captured_upper))
        if dupe_image_names:
            original_caps_table = {pair[0]: pair[1] for pair in zip(original_upper, self.original_images_table.keys())}
            captured_caps_table = {pair[0]: pair[1] for pair in zip(captured_upper, self.captured_images_table.keys())}
            original_dupes = [original_caps_table[dupe_cap_name] for dupe_cap_name in dupe_image_names]
            captured_dupes = [captured_caps_table[dupe_cap_name] for dupe_cap_name in dupe_image_names]
            all_name_dupes = list(set(original_dupes + captured_dupes))
            print("Error: Duplicated image file names between OriginalImages and CapturedImages in %s." % self.bundle_path)
            print("\t%s", str(all_name_dupes))
            print("Exiting")
            sys.exit()
            #TODO: Issue and error dialog here
        self.image_name_to_path_table = {}
        self.image_name_to_path_table.update(self.original_images_table)
        self.image_name_to_path_table.update(self.captured_images_table)
        #TODO: Test that this duplicate detector stuff works

    def image_path_for_name(self, image_name):
        if image_name not in self.image_name_to_path_table:
            print("Error: Unknown image name %s, exiting." % image_name)
            sys.exit()
        return self.image_name_to_path_table[image_name]

    def image_names(self):
        return self.image_name_to_path_table.keys()












































