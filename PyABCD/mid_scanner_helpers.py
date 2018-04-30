import os

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
    with open(rt_file_path, 'w') as f:
        f.write(str(earnings))

    return bool(operator_table['session_number'] == 2 or run_num == 2)





















