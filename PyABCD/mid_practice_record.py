
from abcd_record import *

column_labels_text = ["ExperimentName",
                      "Subject",
                      "Session",
                      "Allowed",
                      "Clock.Information",
                      "DataFile.Basename",
                      "Display.RefreshRate",
                      "ExperimentVersion",
                      "Group",
                      "Handedness",
                      "IntNewRT",
                      "NARGUID",
                      "NewRT",
                      "ProbeDuration",
                      "RandomSeed",
                      "RuntimeCapabilities",
                      "RuntimeVersion",
                      "RuntimeVersionExpected",
                      "SessionDate",
                      "SessionStartDateTimeUtc",
                      "SessionTime",
                      "StudioVersion",
                      "Block",
                      "BlockTitle",
                      "IFISBlockList",
                      "IFISBlockList.Cycle",
                      "IFISBlockList.Sample",
                      "Instruction1",
                      "Instruction2",
                      "ListName",
                      "NameOfPeriodList",
                      "Periods",
                      "Procedure[Block]",
                      "Running[Block]",
                      "Task",
                      "TimingBlockList",
                      "TimingBlockList.Cycle",
                      "TimingBlockList.Sample",
                      "Trial",
                      "PeriodList",
                      "PeriodList.Cycle",
                      "PeriodList.Sample",
                      "PeriodListTiming",
                      "PeriodListTiming.Cycle",
                      "PeriodListTiming.Sample",
                      "Procedure[Trial]",
                      "Running[Trial]",
                      "SubTrial",
                      "Anticipation.RESP",
                      "Condition",
                      "Cue",
                      "LoseBig",
                      "LoseSmall",
                      "Neutral",
                      "prbacc",
                      "Probe",
                      "Probe.ACC",
                      "Probe.DurationError",
                      "Probe.OnsetDelay",
                      "Probe.OnsetTime",
                      "Probe.OnsetToOnsetTime",
                      "Probe.RESP",
                      "Probe.RT",
                      "Procedure[SubTrial]",
                      "ResponseCheck",
                      "Result",
                      "RunList",
                      "RunList.Cycle",
                      "RunList.Sample",
                      "RunListTiming",
                      "RunListTiming.Cycle",
                      "RunListTiming.Sample",
                      "Running[SubTrial]",
                      "WinBig",
                      "WinSmall"]

dummy_constant_columns = [ ("ExperimentName", "ABCD_MID_Practice_20161209"),
                           ("Allowed", "{ANY}"),
                           ("RuntimeCapabilities", "Professional")]


first_trails_nulls = ["BlockTitle",
                      "NameOfPeriodList",
                      "Periods",
                      "TimingBlockList",
                      "TimingBlockList.Cycle",
                      "TimingBlockList.Sample",
                      "PeriodListTiming",
                      "PeriodListTiming.Cycle",
                      "PeriodListTiming.Sample",
                      "RunListTiming",
                      "RunListTiming.Cycle",
                      "RunListTiming.Sample",
                      "RunListTiming.Sample"]


second_trails_nulls = ["IFISBlockList",
                       "IFISBlockList.Cycle",
                       "IFISBlockList.Sample",
                       "Instruction1",
                       "Instruction2",
                       "ListName",
                       "PeriodList",
                       "PeriodList.Cycle",
                       "PeriodList.Sample",
                       "LoseBig",
                       "LoseSmall",
                       "Neutral",
                       "RunList",
                       "RunList.Cycle",
                       "RunList.Sample",
                       "WinBig",
                       "WinSmall"]


class MidPracticeRecord(AbcdRecord):

    def __init__(self, output_dir_path, file_name):
        super(MidPracticeRecord, self).__init__(output_dir_path, file_name, column_labels_text)
        self.add_batch_constant_columns(dummy_constant_columns)


def test_practice_record():
    record = MidPracticeRecord("C:\Users\Allen W. Ingling\Desktop", "test_mid_output")
    record.add_new_row()
    record.add_cell_value_to_row("DataFile.Basename", "Foo")
    record.add_new_row()
    record.add_cell_value_to_row("DataFile.Basename", "Bar")
    record.save()



