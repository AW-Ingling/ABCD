# annex.py
#
#  Various stuff cut out of development code which we might eventually want but is cluttering up the running code


import itertools
import string
from psychopy import visual


def letter_index_to_column_index(letter_index):
    cindex = 0
    for index, letter in enumerate(letter_index[::-1]):
        cindex +=  26**index * (string.lowercase.index(letter.lower()) + 1)
    return cindex


# Make a list of pairs of index, letter_combination where index is the lexicographic index of the
# letter string according to our column numbering scheme defined by letter_index_to_column_index().
# used to test letter_index_to_column_index
def make_test_index_letter_pairs(num_letter_digits):
    letter_combs = itertools.product(string.ascii_lowercase, repeat=num_letter_digits)
    pairs = [(index, "".join(letter_comb)) for index, letter_comb in enumerate(letter_combs)]
    return pairs

# NOTE: this is not quite right because we need to offset the indices by all lower num_alpha_digits length lists.
#
def test_litcoi(num_alpha_digits):
    test_set = make_test_index_letter_pairs(num_alpha_digits)
    for index_and_alpha_num in test_set:
        calculated_index = letter_index_to_column_index(index_and_alpha_num[1])



    def add_subject_id(self, subject_id):
        self.add_constant_column("B", subject_id)

    def add_allowed(self, allowed_value):
        self.add_constant_column("D", allowed_value)

    def add_clock_information(self, clock_info):
        self.add_constant_column("E", clock_info)

    def add_datafile_basename(self, basename):
        self.add_constant_column("F", basename)

    def add_display_refresh_rate(self, refresh_rate_hz):
        self.add_constant_column("G", refresh_rate_hz)

    def add_experiment_version(self, experiment_version):
        self.add_constant_column("H", experiment_version)

    def add_group(self, group_num):
        self.add_constant_column("I", group_num)

    def add_handedness(self, hand):
        self.add_constant_column("J", hand)

    def add_narguid(self, narguid):
        self.add_constant_column("L", narguid)

    def add_runtime_capabilities(self, capabilities):
        self.add_constant_column("P", capabilities)

    def add_runtime_version(self, runtime_version):
        self.add_constant_column("Q", runtime_version)

    def add_runtime_version_expected(self, runtime_version):
        self.add_constant_column("R", runtime_version)



########################################################################################################################


# ExperimentName: a dummy constant column
# Subject: to be completed by a constant column
# Session: to be completed by a constant column
# Allowed: a dummy constant column
# Clock.Information: to be completed by a constant column
# DataFile.Basename: constant column
# Display.RefreshRate: to be completed by a constant column
# ExperimentVersion: a dummy constant column
# Group: constant column
# Handedness: constant column

#output_record.add_cell_value_to_row("IntNewRT", )

# NARGUID: constant column

#output_record.add_cell_value_to_row("NewRT", )
#output_record.add_cell_value_to_row("ProbeDuration", )

# RandomSeed: to be completed by a constant column
# RuntimeCapabilities: a dummy constant column
# RuntimeVersion: a dummy constant column
# RuntimeVersionExpected: a dummy constant column
# SessionDate: constant column
# SessionStartDateTimeUtc: always empty
# SessionTime: constant column
# StudioVersion: a dummy constant column

#output_record.add_cell_value_to_row("Block", )
#output_record.add_cell_value_to_row("BlockTitle", )

# IFISBlockList: second trial NULL
# IFISBlockList.Cycle: second trial NULL
# IFISBlockList.Sample: second trial NULL
# Instruction1: second trial NULL
# Instruction2: second trial NULL
# ListName: second trial NULL

#output_record.add_cell_value_to_row("NameOfPeriodList", )
#output_record.add_cell_value_to_row("Periods", )
#output_record.add_cell_value_to_row("Procedure[Block]", )
#output_record.add_cell_value_to_row("Running[Block]", )


# Task: inter_test_loop_nulls

#output_record.add_cell_value_to_row("TimingBlockList", )
#output_record.add_cell_value_to_row("TimingBlockList.Cycle", )
#output_record.add_cell_value_to_row("TimingBlockList.Sample", )
#output_record.add_cell_value_to_row("Trial", )


# PeriodList: second trail NULL
# PeriodList.Cycle: second trial NULL
# PeriodList.Sample: second trail NULL

#output_record.add_cell_value_to_row("PeriodListTiming", )
#output_record.add_cell_value_to_row("PeriodListTiming.Cycle", )
#output_record.add_cell_value_to_row("PeriodListTiming.Sample", )
#output_record.add_cell_value_to_row("Procedure[Trial]", )
#output_record.add_cell_value_to_row("Running[Trial]", )


# SubTrial: inter_test_loop_nulls
# Anticipation.RESP: inter_test_loop_nulls
# Condition: inter_test_loop_nulls
# Cue: inter_test_loop_nulls
# LoseBig: second trail NULL
# LoseSmall: second trail NULL
# Neutral: second trial NULL
# prbacc: inter_test_loop_nulls
# Probe: inter_test_loop_nulls
# Probe.ACC: inter_test_loop_nulls
# Probe.DurationError: inter_test_loop_nulls
# Probe.OnsetDelay: inter_test_loop_nulls
# Probe.OnsetTime: inter_test_loop_nulls
# Probe.OnsetToOnsetTime: inter_test_loop_nulls
# Probe.RESP: inter_test_loop_nulls
# Probe.RT": inter_test_loop_nulls
# Procedure[SubTrial]: inter_test_loop_nulls
# ResponseCheck: inter_test_loop_nulls
# Result: inter_test_loop_nulls
# RunList: second trail NULL
# RunList.Cycle: second trial NULL
# RunList.Sample: second trial NULL
# RunListTiming: inter_test_loop_nulls
# RunListTiming.Cycle: inter_test_loop_nulls
# RunListTiming.Sample: inter_test_loop_nulls
# Running[SubTrial]: inter_test_loop_nulls
# WinBig: second trail NULL
# WinSmall: second trail NULL


########################################################################################################################


        output_record.add_cell_value_to_row("PracticeRT", )
        output_record.add_cell_value_to_row("RandomSeed", )
        output_record.add_cell_value_to_row("RuntimeCapabilities", )
        output_record.add_cell_value_to_row("RuntimeVersion", )
        output_record.add_cell_value_to_row("RuntimeVersionExpected", )
        output_record.add_cell_value_to_row("SessionDate", )
        output_record.add_cell_value_to_row("SessionStartDateTimeUtc", )
        output_record.add_cell_value_to_row("SessionTime", )
        output_record.add_cell_value_to_row("StudioVersion", )
        output_record.add_cell_value_to_row("TrialOrder", )
        output_record.add_cell_value_to_row("StudioVersion", )
        output_record.add_cell_value_to_row("TrialOrder", )
        output_record.add_cell_value_to_row("triggercode", )
        output_record.add_cell_value_to_row("Block", )
        output_record.add_cell_value_to_row("BlockList", )
        output_record.add_cell_value_to_row("BlockList.Cycle", )
        output_record.add_cell_value_to_row("BlockList.Sample", )
        output_record.add_cell_value_to_row("BlockTitle", )
        output_record.add_cell_value_to_row("EndFix.Duration", )
        output_record.add_cell_value_to_row("EndFix.DurationError", )
        output_record.add_cell_value_to_row("EndFix.FinishTime", )
        output_record.add_cell_value_to_row("EndFix.OffsetDelay", )
        output_record.add_cell_value_to_row("EndFix.OffsetTime", )
        output_record.add_cell_value_to_row("EndFix.OnsetDelay", )
        output_record.add_cell_value_to_row("EndFix.OnsetTime", )
        output_record.add_cell_value_to_row("EndFix.OnsetToOnsetTime", )
        output_record.add_cell_value_to_row("EndFix.StartTime", )
        output_record.add_cell_value_to_row("Procedure[Block]", )
        output_record.add_cell_value_to_row("Running[Block]", )
        output_record.add_cell_value_to_row("Trial", )
        output_record.add_cell_value_to_row("GetReady.RTTime", )

        output_record.add_cell_value_to_row("PeriodList", "NULL")
        output_record.add_cell_value_to_row("PeriodList.Cycle", "NULL")
        output_record.add_cell_value_to_row("PeriodList.Sample", "NULL")
        output_record.add_cell_value_to_row("PrepTime.Duration", "NULL")
        output_record.add_cell_value_to_row("PrepTime.DurationError", "NULL")
        output_record.add_cell_value_to_row("PrepTime.FinishTime", "NULL")
        output_record.add_cell_value_to_row("PrepTime.OffsetDelay", "NULL")
        output_record.add_cell_value_to_row("PrepTime.OffsetTime", "NULL")
        output_record.add_cell_value_to_row("PrepTime.OnsetDelay", "NULL")
        output_record.add_cell_value_to_row("PrepTime.OnsetTime", "NULL")
        output_record.add_cell_value_to_row("PrepTime.OnsetToOnsetTime", "NULL")
        output_record.add_cell_value_to_row("PrepTime.StartTime", "NULL")

        output_record.add_cell_value_to_row("Procedure[Trial]", )
        output_record.add_cell_value_to_row("Waiting4ScannerGE", )
        output_record.add_cell_value_to_row("Waiting4ScannerGE", )
        output_record.add_cell_value_to_row("Waiting4ScannerGE.Cycle", )
        output_record.add_cell_value_to_row("Waiting4ScannerGE.Sample", )