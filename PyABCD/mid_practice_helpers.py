
import numpy

# Code from E-prime "Result" inline in ABCD_MID_Practice:
#
# Select Case c.GetAttrib("Condition")
#
#Case "SmallReward"
#If c.GetAttrib("prbacc") = 1 Then
#	c.SetAttrib "Result", "You earn $0.20!"
#Else
#	c.SetAttrib "Result", "You did not earn $0.20!"
#End If
#
#Case "LgReward"
#If c.GetAttrib("prbacc") = 1 Then
#	c.SetAttrib "Result", "You earn $5!"
#Else
#	c.SetAttrib "Result", "You did not earn $5!"
#End If
#
#Case "SmallPun"
#If c.GetAttrib("prbacc") = 1 Then
#	c.SetAttrib "Result", "You keep $0.20!"
#Else
#	c.SetAttrib "Result", "You lose $0.20!"
#End If
#
#Case "LgPun"
#If c.GetAttrib("prbacc") = 1 Then
#	c.SetAttrib "Result", "You keep $5!"
#Else
#	c.SetAttrib "Result", "You lose $5!"
#End If
#
#Case "Triangle"
#	c.SetAttrib "Result", "No money at stake!"
#End Select


def result_inline(tbl_condition, prbacc_flag):

    message_table = {"SmallReward": {1:"You earn $0.20!", 0:"You did not earn $0.20!"},
                     "LgReward": {1:"You earn $5!", 0:"You did not earn $5!"},
                     "SmallPun": {1:"You keep $0.20!", 0:"You lose $0.20!"},
                     "LgPun": {1:"You keep $5!", 0:"You lose $5!"},
                     "Triangle": {1:"No money at stake!", 0:"No money at stake!"}
                     }

    # convert flag into table index
    if prbacc_flag:
        prbacc_flag_norm = 1
    else:
        prbacc_flag_norm = 0

    return message_table[tbl_condition][prbacc_flag_norm]



# Code from E-prime "CheckResponse" inline in ABCD_MID_Practice:

#  If Len(Anticipation.RESP) > 0 Then
# 	c.SetAttrib "ResponseCheck", "You pressed too soon!"
# 	c.SetAttrib "prbacc", 0
#
# ElseIf Len(Probe.RESP) > 0 Then
#
# 	c.SetAttrib "ResponseCheck", "Correct Response!"
# 	c.SetAttrib "prbacc", 1
#
# Else
# 	c.SetAttrib "ResponseCheck", "You pressed too slow!"
# 	c.SetAttrib "prbacc", 0
#
# End If


def check_response_inline(anticipation_keypress_flag, probe_keypress_flag):

    response_check = None
    prbacc = None

    if anticipation_keypress_flag:
        response_text = "You pressed too soon!"
        prbacc = 0
    elif probe_keypress_flag:
        response_text = "Correct Response!"
        prbacc = 1
    else:
        response_text = "You pressed too slow!"
        prbacc = 0

    return response_text, prbacc


# TODO: Verify this by comparing calculations in E-Prime and this function
class EprimeSummation():

    def __init__(self):
        self.observations = []

    def add_observation(self, obs):
        if obs is not None and obs > 0.100:
            self.observations.append(obs)

    # We have to make sure that we use the variant of std() which matches the one used in E-Prime.  E-Basic provides two
    # std functions, StdDevP and StdDevS but does not document which does what.  The convention outside fo E-Basic
    # (see: https://support.office.com/en-us/article/stdev-stdevp-functions-90a8dbeb-3fd1-485f-9065-bb7b0cdda72e)is:
    #
    #  StDev  - Evaluates a population
    #  StDevS - Evaluates a population sample
    #
    # Assuming E-Basic adhered to that convetion except for adding a "P" to "StDev", then
    #
    #  StDevP  - Evaluates a population
    #  StDevS - Evaluates a population sample
    #
    # The the difference between the population and population sample calculations is the divisor for its mean
    # calculation is:
    #
    # Population            -  average is sum of differences / n
    # Population Sample     -  average is sum of differences / n-1
    #
    # (see https://statistics.laerd.com/statistical-guides/measures-of-spread-standard-deviation.php)
    #
    # The ABCD MID practice uses StdS, therefore we want the n-1, to get that in Python:
    #
    # np.std([sample_1, sample_2,...sample_n], ddof=1)
    #
    # (see https://docs.scipy.org/doc/numpy-1.13.0/reference/generated/numpy.std.html)
    #
    def std_devs(self):
        obs_std = numpy.std(self.observations, ddof=1)
        return obs_std

    def mean(self):
        obs_mean = numpy.mean(self.observations)
        return obs_mean

    def user_rt(self):
        rounded_user_rt = round(self.mean() + 2 * self.std_devs())
        return rounded_user_rt













