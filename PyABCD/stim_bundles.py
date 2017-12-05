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
    def bundle_name_path_pairs(cls):
        if os.path.isdir(cls.bundles_dir_path):
            all_dir_names = os.listdir(cls.bundles_dir_path)
            all_dir_paths = [os.path.join(cls.bundles_dir_path, dir_name) for dir_name in all_dir_names]
            return [pair for pair in zip(all_dir_names, all_dir_paths) if cls.is_bundle(pair[1])]
        else:
            return []

























