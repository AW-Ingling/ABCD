from stim_bundle import *

from stim_bundle import *
from abcd_recnames import *

version_keeper.assign_experiment_types(ExperimentType.mid, ScannerType.practice)
b = StimBundle("mid_practice")
m = make_record_file_name_maker(b)
filename, filename_wo_extension = m("AANNNAAA", 1)


