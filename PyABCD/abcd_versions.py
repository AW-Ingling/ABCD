
from enum import Enum
from abcd_exceptions import *



class ExperimentType(Enum):
    mid = 1

class ScannerType(Enum):
    practice = 1
    ge = 2
    siemens = 3
    debug = 4


# Define some tables constants indexed by the experiment type and/or the scanner type.

RECORD_FILE_PREFIX_TABLE = {ExperimentType.mid: {ScannerType.practice: "ABCD_MID_Practice_20161209_",
                                                 ScannerType.ge: "ABCD_MID_GE_20161218_",
                                                 ScannerType.siemens: "PUT_REAL_MID_PREFIX_HERE_"}}

WAITING_TABLE_FILE_NAME_TABLE = {ExperimentType.mid: {ScannerType.practice: None,  #TODO:fill this in
                                                      ScannerType.ge: "Waiting4ScannerGE",
                                                      ScannerType.siemens: None}}  #TODO:fill this in


SCANNER_TRIGGER_CODE_TABLE = {ScannerType.practice: None,   #TODO:fill this in
                              ScannerType.ge: "^57=",
                              ScannerType.siemens: None}    #TODO:fill this in


EXPERIMENT_NAME_TABLE = {ExperimentType.mid: {ScannerType.practice: None,       #TODO:fill this in
                                                 ScannerType.ge: "MID_GE_20161218",
                                                 ScannerType.siemens: None}}    #TODO:fill this in


RUNNING_TRIAL_HEADER_CELL_VALUES = {ScannerType.practice: None,               #TODO:fill this in
                                    ScannerType.ge: "Waiting4ScannerGE",
                                    ScannerType.siemens: None}                #TODO:fill this in







#TODO: Make this a singleton class
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
        return RECORD_FILE_PREFIX_TABLE[self.experiment_type][self.scanner_type]

    def waiting_table_file_name(self):
        return WAITING_TABLE_FILE_NAME_TABLE[self.experiment_type][self.scanner_type]

    def trigger_code(self):
        return SCANNER_TRIGGER_CODE_TABLE[self.scanner_type]

    def experiment_name(self):
        return EXPERIMENT_NAME_TABLE[self.experiment_type][self.scanner_type]

    def running_trial_header_cell_value(self):
        return RUNNING_TRIAL_HEADER_CELL_VALUES[self.scanner_type]


version_keeper = VersionKeeper()





