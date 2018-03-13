# abcd_recnames.py
#
# Generates and matches record filenames according to naming convention defined by ABCD E-Prime scripts, with some changes
# to the convention for Python versions
#

# NOTES:
# E-Prime style file name: ABCD_MID_Practice_20161209_AANNNAAA-1.xls
#          revised format: ABCD_MID_Practice_20161209_AANNNAAA-1-1.xls

import os
import re
import collections
from abcd_versions import *


DATA_OUTPUT_TABLE_SUFFIX = ".xls"


def has_record_file_extension(name_or_path):
    return os.path.splitext(name_or_path).upper() == DATA_OUTPUT_TABLE_SUFFIX.upper()


def make_output_filename_wo_extension(subject_id, session_number, file_number=1):

    file_name = version_keeper.record_prefix() + subject_id + "-" + str(session_number) + "-" + str(file_number)
    return file_name


def make_output_filename_w_extension(subject_id, session_number, file_number=1):

    file_name = make_output_filename_wo_extension(subject_id, session_number, file_number) + DATA_OUTPUT_TABLE_SUFFIX
    return file_name


def make_name_matcher(regex, index_positions, return_tuple_type):

    re_compiled= re.compile(regex)

    def matcher(a_name):
        m= re_compiled.match(a_name)
        if m is None:
            return False
        if m.start() != 0:
            return False
        if m.end() != len(a_name):
            return False
        tuple_args= []
        for position in index_positions:
            tuple_args.append(m.groups()[position])
        indices= return_tuple_type(*tuple_args)
        return indices

    return matcher

# revised format: ABCD_MID_Practice_20161209_AANNNAAA-1-1.xls

RecordNameFields= collections.namedtuple("RecordNameFields", ["prefix", "subject", "session", "file_number"])
abcd_name_matcher= make_name_matcher("\A(\w+_\d+_)([a-zA-Z]+)-(\d+)-(\d+).xls\Z", [0, 1, 2, 3], RecordNameFields)

# "\A([a-zA-Z_]+)_(\d+)_([a-zA-Z]+)-(\d+)-(\d+).xls\Z"
# "\A([a-zA-Z_]+_\d+_)([a-zA-Z]+)-(\d+)-(\d+).xls\Z"

class RecordFileName():

    @classmethod
    def make(cls, file_path):
        file_name = os.path.split(file_path)[1]
        fields_tuple = abcd_name_matcher(file_name)
        if fields_tuple:
            return RecordFileName(file_path, file_name, fields_tuple)
        else:
            return None

    def __init__(self, full_path, file_name, fields_tuple):
        self.full_path = full_path
        self.file_name = file_name
        self.fields_tuple = fields_tuple

    @property
    def prefix(self):
        return getattr(self.fields_tuple, "prefix")

    @property
    def subject(self):
        return getattr(self.fields_tuple, "subject")

    @property
    def session(self):
        return int(getattr(self.fields_tuple, "session"))

    @property
    def file_number(self):
        return int(getattr(self.fields_tuple, "file_number"))

    def match(self, prefix, subject, session):
        return prefix.upper() == self.prefix.upper() and subject.upper() == self.subject.upper() and session == self.session


#  A class which inventories all of the data files within the directory at data_dir_path and generates the name
#  of a new file within the same directory which does not conflict with existing names.
class RecordFileNameKeeper:

    def __init__(self, data_dir_path):
        self.data_dir_path = data_dir_path
        self.record_files = []

    def dir_inventory(self):
        all_contents_names = os.listdir(self.data_dir_path)
        all_contents_paths = [os.path.join(self.data_dir_path, name) for name in all_contents_names]
        all_file_paths = [path for path in all_contents_paths if os.path.isfile(path)]
        return [rfile for rfile in [RecordFileName.make(path) for path in all_file_paths] if rfile]

    # def make_new_record_path(self, prefix, subject_id, session_number):
    #     self.record_files = self.dir_inventory()
    #     matched_files = [rfile for rfile in self.record_files if rfile.match(prefix, subject_id, session_number)]
    #     matched_file_numbers = [rfile.file_number for rfile in matched_files]
    #     matched_file_numbers.append(0)  # add zero in case of empty
    #     new_file_number = max(matched_file_numbers) + 1
    #     new_file_name = make_output_filename_w_extension(subject_id, session_number, new_file_number)
    #     new_file_path = os.path.join(self.data_dir_path, new_file_name)
    #     return new_file_path

    def make_new_record_filename(self, prefix, subject_id, session_number):
        self.record_files = self.dir_inventory()
        matched_files = [rfile for rfile in self.record_files if rfile.match(prefix, subject_id, session_number)]
        matched_file_numbers = [rfile.file_number for rfile in matched_files]
        matched_file_numbers.append(0)  # add zero in case of empty
        new_file_number = max(matched_file_numbers) + 1
        new_file_name = make_output_filename_w_extension(subject_id, session_number, new_file_number)
        new_file_name_wo_extension = make_output_filename_wo_extension(subject_id, session_number, new_file_number)
        return new_file_name, new_file_name_wo_extension

# accept a stim_bundle instance and return a function which makes the name of a new output data file
def make_record_file_name_maker(stim_bundle):

    data_dir_path = stim_bundle.data_dir_path
    prefix = version_keeper.record_prefix()

    def make_file_path(subject_id, session_number):
        file_keeper = RecordFileNameKeeper(data_dir_path)
        new_filename, new_filename_wo_extension = file_keeper.make_new_record_filename(prefix, subject_id, session_number)
        return new_filename, new_filename_wo_extension

    return make_file_path


