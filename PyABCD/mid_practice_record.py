
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


class MidPracticeRecord(AbcdRecord):

    def __init__(self, output_dir_path, file_name, column_labels_text, constant_columns_table):
        super(MidPracticeRecord, self).__init__(output_dir_path, file_name, column_labels_text)
        self.add_batch_constant_columns(constant_columns_table)



record = MidPracticeRecord("C:\Users\Allen W. Ingling\Desktop", "test_mid_output", column_labels_text, dummy_constant_columns)
record.add_new_row()
record.add_new_row()
record.save()


