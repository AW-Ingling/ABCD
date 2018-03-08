# abcd_recnames.py
#
# Generates and matches record filenames according to naming convention defined by ABCD E-Prime scripts, with some changes
# to the convention for Python versions
#

from abcd_versions import *


DATA_OUTPUT_TABLE_SUFFIX = ".xls"



def make_output_filename_wo_extension(subject_id, session_number):

    file_name = version_keeper.record_prefix() + subject_id + "-" + str(session_number)
    return file_name


def make_output_filename_w_extension(subject_id, session_number):

    file_name = make_output_filename_wo_extension(subject_id, session_number) + DATA_OUTPUT_TABLE_SUFFIX
    return file_name


