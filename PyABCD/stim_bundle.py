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

    image_sets_dir_name = u'StimulusSets'
    original_image_dir_name = u'OriginalImages'
    captured_image_dir_name = u'CapturedImages'
    tables_dir_name  =u'Tables'


    @classmethod
    def original_dir_path_from_bundle_path(cls, bundle_path):
        return os.path.join(bundle_path, cls.original_image_dir_name)

    @classmethod
    def captured_dir_path_from_bundle_path(cls, bundle_path):
        return os.path.join(bundle_path, cls.captured_image_dir_name)

    @classmethod
    def tables_dir_path_from_bundle_path(cls, bundle_path):
        return os.path.join(bundle_path, cls.tables_dir_name)

    @classmethod
    def is_bundle(cls, path_to_bundle):
        return (os.path.isdir(path_to_bundle)
                and os.path.isdir(cls.original_dir_path_from_bundle_path(path_to_bundle))
                and os.path.isdir(cls.captured_dir_path_from_bundle_path(path_to_bundle))
                and os.path.isdir(cls.tables_dir_path_from_bundle_path(path_to_bundle)))

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
            print("Error: Directory contains duplicate image file names, Exiting.")
            print("\tdirectory: %s." % image_dir_path)
            print("\tduplicates: %s." % str(duplicate_names))
            sys.exit()
            #TODO: Issue and error dialog here
            # TODO: Test that this duplicate detector stuff works
        image_file_paths = [os.path.join(image_dir_path, file_name) for file_name in image_file_names]
        image_path_table = {pair[0]: pair[1] for pair in zip(image_names, image_file_paths)}
        return image_path_table

    #TODO: image_table_from_path() and tables_table_from_path() could be abstracted and consolidated.
    @staticmethod
    def excel_paths_table_from_path(tables_dir_path):
        all_file_names = os.listdir(tables_dir_path)
        table_file_names = [filename for filename in all_file_names if is_table_file(filename)]
        table_names = [os.path.splitext(filename)[0] for filename in table_file_names]
        table_names_caps = [name.upper() for name in table_names]
        duplicate_table_cap_names = find_duplicates(table_names_caps)
        if duplicate_table_cap_names:
            name_cap_table = {pair[0]:pair[1] for pair in zip(table_names_caps, table_names)}
            duplicate_names = [name_cap_table[cap_name] for cap_name in duplicate_table_cap_names]
            print("Error: Directory contains duplicate table file names, Exiting.")
            print("\tdirectory: %s." % tables_dir_path)
            print("\tduplicates: %s." % str(duplicate_names))
            sys.exit()
            #TODO: Issue and error dialog here
            # TODO: Test that this duplicate detector stuff works
        table_file_paths = [os.path.join(tables_dir_path, file_name) for file_name in table_file_names]
        table_path_table = {pair[0]: pair[1] for pair in zip(table_names, table_file_paths)}
        return table_path_table

    # @staticmethod
    # def excel_file_name_from_table_name(table_name):
    #     #TODO: handle filenames with upper-case .xls extension
    #     base, ext = os.path.splitext(table_name)
    #     if ext == ".xls":
    #         return table_name
    #     else:
    #         return table_name + ".xls"

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
        self.tables_path = self.tables_dir_path_from_bundle_path(self.bundle_path)
        # generate a table mapping from the image name to image file path.  We merge the
        # tables for contents of both the original and captured image directories and test
        # for duplicates
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
        # merge the two tables
        self.image_name_to_path_table = {}
        self.image_name_to_path_table.update(self.original_images_table)
        self.image_name_to_path_table.update(self.captured_images_table)
        #TODO: Test that this duplicate detector stuff works
        # generate a table mapping from the table name to the table file path
        self.table_name_to_excel_file_path_table = self.excel_paths_table_from_path(self.tables_path)

    def image_names(self):
        return self.image_name_to_path_table.keys()

    def table_names(self):
        return self.table_name_to_excel_file_path_table.keys()

    def image_path_for_name(self, image_name):
        if image_name not in self.image_name_to_path_table:
            #TODO: Display an error dialog here
            print("Error: Unknown image name %s, exiting." % image_name)
            sys.exit()
        return self.image_name_to_path_table[image_name]

    def excel_file_path_for_table_name(self, table_name):
        if table_name not in self.table_name_to_excel_file_path_table:
            #TODO: Display an error dialog here
            print("Error: Unknown table name %s, exiting." % table_name)
            sys.exit()
        return self.table_name_to_excel_file_path_table[table_name]

















































