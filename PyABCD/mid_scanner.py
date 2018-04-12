

# References:
#
# Keyboard input in E-Prime:
# http://www.e-primer.com/2015/06/special-keys-in-e-prime.html
#
#

from abcd_versions import *
from abcd_show import *
from abcd_table import *
import abcd_random

# define the experiment and scanner type
version_keeper.assign_experiment_types(ExperimentType.mid, ScannerType.ge)

# init our random number generator so so that we can get the seed for the table
rand_gen = abcd_random.ABCDRandom()

# Get the stimulus bundle object which manages stimulus images, tables and text files for the project
stim_bundle = StimBundle("mid_scanner")





