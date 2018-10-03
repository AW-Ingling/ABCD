
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
                      "NARGUID",
                      "PracticeRT",
                      "RandomSeed",
                      "RuntimeCapabilities",
                      "RuntimeVersion",
                      "RuntimeVersionExpected",
                      "SessionDate",
                      "SessionStartDateTimeUtc",
                      "SessionTime",
                      "StudioVersion",
                      "TrialOrder",
                      "triggercode",
                      "Block",
                      "BlockList",
                      "BlockList.Cycle",
                      "BlockList.Sample",
                      "BlockTitle",
                      "EndFix.Duration",
                      "EndFix.DurationError",
                      "EndFix.FinishTime",
                      "EndFix.OffsetDelay",
                      "EndFix.OffsetTime",
                      "EndFix.OnsetDelay",
                      "EndFix.OnsetTime",
                      "EndFix.OnsetToOnsetTime",
                      "EndFix.StartTime	",
                      "Procedure[Block]",
                      "Running[Block]",
                      "Trial",
                      "GetReady.RTTime",
                      "PeriodList",
                      "PeriodList.Cycle",
                      "PeriodList.Sample",
                      "PrepTime.Duration",
                      "PrepTime.DurationError",
                      "PrepTime.FinishTime",
                      "PrepTime.OffsetDelay",
                      "PrepTime.OffsetTime",
                      "PrepTime.OnsetDelay",
                      "PrepTime.OnsetTime",
                      "PrepTime.OnsetToOnsetTime",
                      "PrepTime.StartTime",
                      "Procedure[Trial]	Running[Trial]",
                      "Waiting4ScannerGE",
                      "Waiting4ScannerGE.Cycle",
                      "Waiting4ScannerGE.Sample",
                      "SubTrial	Anticipation.Duration",
                      "Anticipation.DurationError",
                      "Anticipation.FinishTime",
                      "Anticipation.OffsetDelay",
                      "Anticipation.OffsetTime",
                      "Anticipation.OnsetDelay",
                      "Anticipation.OnsetTime",
                      "Anticipation.OnsetToOnsetTime",
                      "Anticipation.StartTime",
                      "AnticipationDuration",
                      "Condition",
                      "Cue",
                      "Cue.CustomOnsetTime",
                      "Cue.Duration",
                      "Cue.DurationError",
                      "Cue.FinishTime",
                      "Cue.OffsetDelay",
                      "Cue.OffsetTime",
                      "Cue.OnsetDelay",
                      "Cue.OnsetTime",
                      "Cue.OnsetToOnsetTime	",
                      "Cue.StartTime",
                      "Feedback.Duration",
                      "Feedback.DurationError",
                      "Feedback.FinishTime",
                      "Feedback.OffsetDelay",
                      "Feedback.OffsetTime",
                      "Feedback.OnsetDelay",
                      "Feedback.OnsetTime",
                      "Feedback.OnsetToOnsetTime",
                      "Feedback.StartTime",
                      "FeedbackDuration",
                      "meanrt",
                      "moneyamt",
                      "percentacc",
                      "prbacc",
                      "prbresp",
                      "prbrt",
                      "Probe",
                      "Probe.Duration",
                      "Probe.DurationError",
                      "Probe.FinishTime",
                      "Probe.OffsetDelay",
                      "Probe.OffsetTime",
                      "Probe.OnsetDelay",
                      "Probe.OnsetTime",
                      "Probe.OnsetToOnsetTime",
                      "Probe.RESP",
                      "Probe.RT",
                      "Probe.RTTime	",
                      "Probe.StartTime",
                      "ProbeTime",
                      "Procedure[SubTrial]",
                      "ResponseCheck",
                      "Result",
                      "RunList",
                      "RunList.Cycle",
                      "RunList.Sample",
                      "RunMoney",
                      "Running[SubTrial]",
                      "TextDisplay1.Duration",
                      "TextDisplay1.DurationError",
                      "TextDisplay1.FinishTime",
                      "TextDisplay1.OffsetDelay",
                      "TextDisplay1.OffsetTime",
                      "TextDisplay1.OnsetDelay",
                      "TextDisplay1.OnsetTime",
                      "TextDisplay1.OnsetToOnsetTime",
                      "TextDisplay1.StartTime",
                      "TimeVersion16",
                      "TimeVersion5"]

dummy_constant_columns = [ ("Clock.Information", "NULL"),
                           ("RuntimeCapabilities", "Professional"),
                           ("ExperimentVersion", "1.0.0.300"),
                           ("RuntimeCapabilities", "Professional"),
                           ("RuntimeVersion", "2.0.10.356"),
                           ("RuntimeVersionExpected", "2.0.10.356"),
                           ("StudioVersion", "2.0.10.252")
                           ]


first_trails_nulls = []

second_trails_nulls = []

inter_test_loop_nulls = ["SubTrial",
                         "Anticipation.Duration",
                         "Anticipation.FinishTime",
                         "Anticipation.OffsetDelay",
                         "Anticipation.OffsetTime",
                         "Anticipation.OnsetDelay",
                         "Anticipation.OnsetTime",
                         "Anticipation.OnsetToOnsetTime",
                         "Anticipation.StartTime",
                         "AnticipationDuration",
                         "Condition",
                         "Cue",
                         "Cue.CustomOnsetTime",
                         "Cue.Duration",
                         "Cue.DurationError",
                         "Cue.FinishTime",
                         "Cue.OffsetDelay",
                         "Cue.OffsetTime",
                         "Cue.OnsetDelay",
                         "Cue.OnsetTime",
                         "Cue.OnsetToOnsetTime",
                         "Cue.StartTime",
                         "Feedback.Duration",
                         "Feedback.DurationError",
                         "Feedback.FinishTime",
                         "Feedback.OffsetDelay",
                         "Feedback.OffsetTime",
                         "Feedback.OnsetDelay",
                         "Feedback.OnsetTime",
                         "Feedback.OnsetToOnsetTime",
                         "Feedback.StartTime",
                         "FeedbackDuration",
                         "meanrt",
                         "moneyamt",
                         "percentacc",
                         "prbacc",
                         "prbresp",
                         "prbrt",
                         "Probe",
                         "Probe.Duration",
                         "Probe.DurationError",
                         "Probe.FinishTime",
                         "Probe.OffsetDelay",
                         "Probe.OffsetTime",
                         "Probe.OnsetDelay",
                         "Probe.OnsetTime",
                         "Probe.OnsetToOnsetTime",
                         "Probe.RESP",
                         "Probe.RT",
                         "Probe.RTTime",
                         "Probe.StartTime",
                         "ProbeTime",
                         "Procedure[SubTrial]",
                         "ResponseCheck",
                         "Result",
                         "RunList",
                         "RunList.Cycle",
                         "RunList.Sample",
                         "RunMoney",
                         "Running[SubTrial]",
                         "TextDisplay1.Duration",
                         "TextDisplay1.DurationError",
                         "TextDisplay1.FinishTime",
                         "TextDisplay1.OffsetDelay",
                         "TextDisplay1.OffsetTime",
                         "TextDisplay1.OnsetDelay",
                         "TextDisplay1.OnsetTime",
                         "TextDisplay1.OnsetToOnsetTime",
                         "TextDisplay1.StartTime",
                         "TimeVersion16",
                         "TimeVersion5"]



class MidScannerRecord(AbcdRecord):

    def __init__(self, output_dir_path, file_name):
        super(MidScannerRecord, self).__init__(output_dir_path, file_name, column_labels_text)
        self.add_batch_constant_columns(dummy_constant_columns)





