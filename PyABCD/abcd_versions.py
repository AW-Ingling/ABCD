
from enum import Enum
from abcd_exceptions import *



class ExperimentType(Enum):
    mid = 1

class ScannerType(Enum):
    practice = 1
    ge = 2
    siemens = 3


RECORD_FILE_PREFIX_TABLE = {ExperimentType.mid: {ScannerType.practice: "ABCD_MID_Practice_20161209_",
                                                 ScannerType.ge: "PUT_REAL_MID_PREFIX_HERE_",
                                                 ScannerType.siemens: "PUT_REAL_MID_PREFIX_HERE_"}}


class VersionKeeper():

    def __init__(self):
        self.experiment_type = None
        self.scanner_type = None

    def assign_experiment_types(self, experiment_type, scanner_type):
        if self.experiment_type or self.scanner_type:
            raise DuplicateVersioning()
        self.experiment_type = experiment_type
        self.scanner_type = scanner_type

    def record_prefix(self):
        return RECORD_FILE_PREFIX_TABLE[self.experiment_type, self.scanner_type]


version_keeper = VersionKeeper()





