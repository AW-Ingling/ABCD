import os
import sys
import numpy

time_version_filename_prefix = "TimeVersion"

trial_order_table = dict()

trial_order_table[0] = {1: 5,
                        2: 13,
                        3: 9,
                        4: 15,
                        5: 6,
                        6: 8,
                        7: 2,
                        8: 3,
                        9: 10,
                        10: 7,
                        11: 11,
                        12: 4}

trial_order_table[1] = {1: 16,
                        2: 1,
                        3: 14,
                        4: 12,
                        5: 5,
                        6: 11,
                        7: 9,
                        8: 8,
                        9: 2,
                        10: 13,
                        11: 7,
                        12: 3}

def time_version_file_name(r_number, trial_order):
    file_number = trial_order_table[r_number][trial_order]
    file_name = time_version_filename_prefix + str(file_number)
    return file_name




# 'This is the starting Probe Duration. This is calculated during the practice MID game.
# 'The probe duration is calculated as the mean RT + 2*Standard Deviation.
# 'This should not be higher than 500 ms!
#
# Dim irtfile As String
# Dim imonfile As String
# Dim runMoney As Double
# Dim intRT As Integer
# Dim s As String
# Set TotalMoney = New Summation
#
# runNum = 1
#
# If c.GetAttrib("Session") = 2 Then
#   runNum = 2
#   irtfile = c.GetAttrib("NARGUID") & "_1_RT.txt"
#   imonfile = c.GetAttrib("NARGUID") & "_1_Earnings.txt"
#
#   If Not FileExists(irtfile) Then
#       intRT = c.GetAttrib("PracticeRT")
#   Else
#       Open irtfile For Input As  # 1
#       Input  # 1,s$
#       intRT = CInt(s$)
#       Close  # 1
#   End If
#
#   If FileExists(imonfile) Then
#       Open imonfile For Input As  # 1
#       Input  # 1,s$
#
#       TotalMoney.AddObservation CDbl(s$)
#       Close  # 1
#   End If
# Else
#   intRT = c.GetAttrib("PracticeRT")
# End If
#
# 'Debug.Print intRT
# 'Debug.Print TotalMoney.Total






# derives the starting MID Scanner rt parameter which depends on the run number, the operator input and cache files
def find_rt_earnings_run_num(operator_table, stim_bundle):

    run_num = 1
    rt = operator_table['average_rt']
    earnings_dollars = 0
    if operator_table['session_number'] == 2:
        # if this is session #2 then the run_num starts at 2
        run_num = 2
        # try to read the rt variable from the cache file
        rt_file_path = stim_bundle.rt_file_path(operator_table['subject_id'], 1)
        if os.path.isfile(rt_file_path):
            with open(rt_file_path, "r") as f:
                rt = int(f.readline())
        # try to read the money from the cache file
        earnings_file_path = stim_bundle.earnings_file_path(operator_table['subject_id'], 1)
        if os.path.isfile(earnings_file_path):
            with open(earnings_file_path) as f:
                earnings_dollars = int(f.readline)

    return rt, earnings_dollars, run_num


# Write the rt value and cumulative earnings values to their respective cache files for this run_num.
# Return a boolean flag indicating if the top-level loop should stop.
def write_rt_earnings(operator_table, stim_bundle, run_num, rt, earnings):

    rt_file_path = stim_bundle.rt_file_path(operator_table['subject_id'], run_num)
    earnings_file_path = stim_bundle.earnings_file_path(operator_table['subject_id'], run_num)
    with open(rt_file_path, 'w') as f:
        f.write(str(rt))
    with open(earnings_file_path, 'w') as f:
        f.write(str(earnings))

    return bool(operator_table['session_number'] == 2 or run_num == 2)



# 	If Len(Anticipation.RESP) > 0 Then
#		c.SetAttrib "ResponseCheck", "You pressed too soon!"
#
#		c.SetAttrib "prbacc", 0
#		c.SetAttrib "prbresp", ""
#		c.SetAttrib "prbrt", 0
#
#
#	ElseIf Len(Probe.RESP) > 0 Then
#
#		c.SetAttrib "ResponseCheck", "Correct Response!"
#
#		c.SetAttrib "prbacc", 1
#		c.SetAttrib "prbresp", Probe.RESP
#		c.SetAttrib "prbrt", Probe.RT
#
#	Else
#		c.SetAttrib "ResponseCheck", "You pressed too slow!"
#
#		c.SetAttrib "prbacc", 0
#		c.SetAttrib "prbresp", Probe.RESP
#		c.SetAttrib "prbrt", Probe.RT
#
#	End If
#
#	Select Case c.GetAttrib("Condition")
#		Case "SmallReward"
#			If c.GetAttrib("prbacc") = 1 Then
#				c.SetAttrib "Result", "You earn $0.20!"
#				c.SetAttrib "RunMoney", 0.20
#			Else
#				c.SetAttrib "Result", "You did not earn $0.20!"
#				c.SetAttrib "RunMoney", 0
#			End If
#
#		Case "LgReward"
#			If c.GetAttrib("prbacc") = 1 Then
#				c.SetAttrib "Result", "You earn $5!"
#				c.SetAttrib "RunMoney", 5
#			Else
#				c.SetAttrib "Result", "You did not earn $5!"
#				c.SetAttrib "RunMoney", 0
#			End If
#		Case "SmallPun"
#			If c.GetAttrib("prbacc") = 1 Then
#				c.SetAttrib "Result", "You keep $0.20!"
#				c.SetAttrib "RunMoney", 0
#			Else
#				c.SetAttrib "Result", "You lose $0.20!"
#				c.SetAttrib "RunMoney", -0.20
#			End If
#
#		Case "LgPun"
#			If c.GetAttrib("prbacc") = 1 Then
#				c.SetAttrib "Result", "You keep $5!"
#				c.SetAttrib "RunMoney", 0
#			Else
#				c.SetAttrib "Result", "You lose $5!"
#				c.SetAttrib "RunMoney", -5
#			End If
#		Case "Triangle"
#				c.SetAttrib "Result", "No money at stake!"
#				c.SetAttrib "RunMoney", 0
#	End Select
#


# inputs:
#   anticipation_response       boolean flag indicating if user responded during anticipation stimulus presentation
#   probe_response              boolean flag indicating if user responded during the probe stimulus presentation
#   condition                   the test condition: "SmallReward", "LgReward", "SmallPun", "LgPun", "Triangle"
#
# outputs:
#   response_ok                 flag indicating if probe was correctly detected
#   message_check               primary response message
#   message                     detail response message
#   money                       how much money to add to the total
#
def find_outcomes(anticipation_pressed, probe_pressed, condition):

  # Determine the "message_check" (primary) reponse string and conditaionlly set a flag variable, response_ok.
  if anticipation_pressed:
      message_check = "You pressed too soon!"
      response_ok = False
  elif probe_pressed:
      message_check = "Correct Response!"
      response_ok = True
  else:
      message_check = "You pressed too slow!"
      response_ok = False

  # Determine the message and money values based on correctness of response and the condition (which stim appeared)
  if condition == "SmallReward":
      if response_ok:
          message = "You earn $0.20!"
          money = 0.20
      else:
          message = "You did not earn $0.20!"
          money = 0.00
  elif condition == "LgReward":
      if response_ok:
          message = "You earn $5!"
          money = 5.00
      else:
          message = "You did not earn $5!"
          money = 0.00
  elif condition == "SmallPun":
      if response_ok:
          message = "You keep $0.20!"
          money = 0.00
      else:
          message = "You lose $0.20!"
          money = -0.20
  elif condition == "LgPun":
      if response_ok:
          message = "You keep $5!"
          money = 0.00
      else:
          message = "You lose $5!"
          money = -5.00
  elif condition == "Triangle":
          message = "No money at stake!"
          money = 0.00
  else:
      print("Error: illegal condition")
      sys.exit()

  return response_ok, message_check, message, money




# Dim TrialTypeStr As String
# Dim TrialType As Integer
# Dim UserPercentAcc As Double
#
# TrialTypeStr = c.GetAttrib("Condition")
#
#	Select Case TrialTypeStr
#		Case "LgReward"
#			TrialType = "1"
#		Case "SmallReward"
#			TrialType = "2"
#		Case "Triangle"
#			TrialType = "3"
#		Case "SmallPun"
#			TrialType = "4"
# 		Case "LgPun"
#			TrialType = "5"
#	End Select
#
#
#
# TotalMoney.AddObservation CDbl(c.GetAttrib("RunMoney"))
# c.SetAttrib "moneyamt", TotalMoney.mean*Trials
#
#
# Feed.AddObservation CDbl(c.GetAttrib("prbacc"))
# c.SetAttrib "percentacc", Feed.Total/Trials*100
#
# If TrialType <> 3 Then
#	If c.GetAttrib("prbrt") > 0 Then
#		MyUserRT.AddObservation c.GetAttrib("prbrt")
#	End If
#	UserAcc.AddObservation CDbl(c.GetAttrib("prbacc"))
#	NonNeutralTrialsNum = NonNeutralTrialsNum + 1
#
#
#
#	'Debug.Print DelimitText("\t", UserPercentAcc, Acc, MyUserRT.Mean, NonNeutralTrialsNum, Trials, Probe.Duration, AdjUserRT, TheProbeDuration)
#
# 	'The probe duration is adjusted every three trials starting at trial 7.
# 	'Acc is calculated using only non-neutral trial types.
#
#
#
#	If NonNeutralTrialsNum = AdjTrial + AdjTrialInc Then
#		UserPercentAcc = UserAcc.Total/3*100
#		If NonNeutralTrialsNum = 3 Then
#			Acc = UserPercentAcc
#		Else
#			Acc = (UserPercentAcc + prevAcc)/2
#		End If
#
#		If Acc < 5 Then
#				AdjUserRT = AdjUserRT + 70
#		ElseIf Acc < 15 Then
#			AdjUserRT = AdjUserRT + 60
#		ElseIf Acc < 25 Then
#			AdjUserRT = AdjUserRT + 50
#		ElseIf Acc < 35 Then
#			AdjUserRT = AdjUserRT + 40
#		ElseIf Acc < 45 Then
#			AdjUserRT = AdjUserRT + 30
#		ElseIf Acc < 55 Then
#			AdjUserRT = AdjUserRT + 20
#		ElseIf Acc > 95 Then
#			AdjUserRT = AdjUserRT - 50
#		ElseIf Acc > 85 Then
#			AdjUserRT = AdjUserRT - 40
#		ElseIf Acc > 75 Then
#			AdjUserRT = AdjUserRT - 30
#		ElseIf Acc > 65 Then
#			AdjUserRT = AdjUserRT - 20
#	 	End If
#
#		Set UserAcc = New Summation
#		prevAcc = UserPercentAcc
#
#		AdjTrial = NonNeutralTrialsNum
#		TheProbeDuration = AdjUserRT
#	End If
# End If
# If MyUserRT.Mean > 0 Then
#	c.SetAttrib "meanrt", MyUserRT.Mean
# End If

# If TheProbeDuration > 500 Then
# 	TheProbeDuration = 500
# 	AdjUserRT = 500
# End If
#
# If TheProbeDuration < 150 Then
# 	TheProbeDuration = 150
# 	AdjUserRT = 150
# End If

# 'Debug.Print DelimitText("\t", TrialType, UserPercentAcc, Acc, prevAcc, c.GetAttrib("prbacc"), MyUserRT.Mean, NonNeutralTrialsNum, Trials, Probe.Duration, AdjUserRT, TheProbeDuration)

# Trials = Trials + 1



class ProbeRecord:

    def __init__(self, condition_name, response_ok, reaction_time_secs, money):
        self.condition_name = condition_name
        self.response_ok = response_ok
        self.reaction_time_secs = reaction_time_secs
        self.money = money

    def is_netural(self):
        return self.condition_name == "Triangle"



# E-Prime variable key:
#
#   E-Prime         ProbeCalculator                     Description
#
#   RunMoney        add_probe(...,money)                Money earned or lost on most recent trial
#   TotalMoney      probes[].money                      List of money amounts earned or lost on each trial
#   moneyamt        total_money                         Sum of money earned on all trials
#   percentacc      percent_acc                         Percentage of all trials with correct response
#   prbrt (msecs)   add_probe(...,reaction_time_secs)   The time from stimulus onset until the user presses resp. key
#   my_user_rt      rts_secs                            reaction times for trials with correct responses and non-neutral probes
#   mean_rt         mean_rts_secs                       mean of  my_user_rt(E-Prime)/rts_secs(ProbeCalculator)
#   

class ProbeCalculator:

    def __init__(self, initial_probe_duration_secs):
        # init state variables and retain arguments
        self.probes = []
        self.num_probes = 0
        self.non_neutral_probes = []
        self.probe_duration_secs = initial_probe_duration_secs
        # variables for tracking and incrememting indices at which we adjust the probe duration
        self.num_non_neutral_probes = 0
        self.adj_index_last = 0
        self.adj_index_inc = 3
        self.response_ok_pool = []

    # Add a new probe to the list of probes
    def add_probe(self, condition_name, response_ok, reaction_time_secs, money):
        probe = ProbeRecord(condition_name, response_ok, reaction_time_secs, money)
        self.probes.append(probe)
        self.num_probes += 1
        # maintain a separate list and count of non-netural probes (instead of filtering for every access)
        if not probe.is_netural:
            self.non_neutral_probes.append(probe)
            self.adjust_probe_duration()
        # conditionally bound probe duration
        self.bound_probe_duration()

    # Return the total money earned.
    @property
    def money_total(self):
        return sum([probe_record.money for probe_record in self.probes])

    # Return the percentage of all trials for for which the user responded correctly
    @property
    def percent_acc(self):
        total_ok = sum([1 if probe_record.response_ok else 0 for probe_record in self.probes])
        percent_ok = float(total_ok) / float(self.num_probes) * 100.0
        return percent_ok

    # List of reaction times for trials with correct responses and non-neutral probes.
    @property
    def rts_secs(self):
        return [probe.reaction_time_secs for probe in self.non_neutral_probes if probe.reaction_time_secs]

    # Mean of reaction times for trials with correct responses and non-neutral probes.
    @property
    def mean_rts_secs(self):
        return numpy.mean(self.rts_secs)

    def adjust_probe_duration(self):
        if self.num_non_neutral_probes == self.adj_index_last + self.adj_index_inc:
            # update the index marking the last time this block was called.
            self.adj_index_last = self.num_non_neutral_probes
            # calculate the mean percent response ok for the previous three non-neutral trials
            self.response_ok_pool_avg = numpy.mean(self.response_ok_pool) * 100.0
            # conditionally calculate a weighed average of the current and previous averages
            if self.num_non_neutral_probes == 3:
                pool_avg2 = self.response_ok_pool_avg
            else:
                pool_avg2 = self.response_ok_pool_avg + self.response_ok_pool_avg_prev / 2.0
            # shift the current average into the previous average variable
            self.response_ok_pool_avg_prev = self.response_ok_pool_avg
            # empty the response pool of three non-neutral trials.
            self.response_ok_pool = []
            # adjust the probe duration according to the weighted average of the average %correct of the
            #  prevoius three trials.
            if  pool_avg2 < 5:
                self.probe_duration_secs += 0.070
            elif pool_avg2 < 15:
                self.probe_duration_secs += 0.060
            elif pool_avg2 < 25:
                self.probe_duration_secs += 0.050
            elif pool_avg2 < 35:
                self.probe_duration_secs += 0.040
            elif pool_avg2 < 45:
                self.probe_duration_secs += 0.030
            elif pool_avg2 < 55:
                self.probe_duration_secs += 0.020
            elif pool_avg2 > 95:
                self.probe_duration_secs -= 0.050
            elif pool_avg2 > 85:
                self.probe_duration_secs -= 0.040
            elif pool_avg2 > 75:
                self.probe_duration_secs -= 0.030
            elif pool_avg2 > 65:
                self.probe_duration_secs -= 0.020

    # Apply bounds limits to the instance variable "prove_duration".
    def bound_probe_duration(self):
        if self.probe_duration_secs > 0.500:
            self.probe_duration_secs = 0.500
        if self.probe_duration_secs < 0.150:
            self.probe_duration_secs = 0.150

    @property
    def feedback_duration_secs(self):
        return 1.950 - self.probe_duration_secs


def display_money_table(total_dollars):
    """ Creates a table of strings to be displayed by shower.show with a TextDisplay type argument.

        Generates a dictionary which conditionally

        Note:
            The automatic vertical centering of shower might cause the height of the text display in the case of
            earnings < $1.00 to mistach the E-Prime version by one line.  TODO: Check text height.

        Args:
            total_dollars (float): The total number of dollars earned.

        Returns:

            dict: Keys correspond to those bracketed within the "DisplayMoney" TextDisplay file:
            earned_line_2, earned_line_3
    """
    # clamp lower bound displayed earnings to $1.00 and conditionally display earnings on one or two lines
    # depending on whether they are equal or below $1.00 or above, respectively.
    if total_dollars <= 1.00:
        earned_line_2 = "You earned a total of: $1.00"
        earned_line_3 = ""
    else:
        earned_line_2 = "You earned a total of:"
        earned_line_3 = '${:,.2f}'.format(total_dollars)
    earn_table = {"earned_line_2": earned_line_2, "earned_line_3": earned_line_3}
    return earn_table





























































