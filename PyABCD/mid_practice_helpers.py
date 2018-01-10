

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
#
#If Len(Anticipation.RESP) > 0 Then
# 	c.SetAttrib "ResponseCheck", "You pressed too soon!"
#	c.SetAttrib "prbacc", 0
#
#ElseIf Len(Probe.RESP) > 0 Then
#
#	c.SetAttrib "ResponseCheck", "Correct Response!"
#	c.SetAttrib "prbacc", 1
#
#Else
#	c.SetAttrib "ResponseCheck", "You pressed too slow!"
#	c.SetAttrib "prbacc", 0
#
#End If

def check_response_inline(anticipation_keypress_flag, probe_keypress_flag):

    response_check = None
    prbacc = None

    if anticipation_keypress_flag:
        response_text = "You pressed too soon!"
        prbacc = 0
    elif probe_keypress_flag:
        response_text = "ResponseCheck", "Correct Response!"
        prbacc = 1
    else:
        response_text = "You pressed too slow!"
        prbacc = 0

    return response_text, prbacc


