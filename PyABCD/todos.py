
# TODO

# - The second stimulus loop is missing one trial, it seems to be a row of nulls, or maybe that is inserted between
#   the first and the second?
# - make sure that the application constructs all paths if they do not yet exist.
# - make all base classes subclasses of object.
# - Fix ms -> seconds units in output
# - Fix text inversion
# - Find out if we need to match CInt behaviour with round in the EprimeSummation class.
# - Remove unneeded stuff from images folders
# - Add the closing screens after the second training loop terminates
# - Terminate practice loop early if the mean rt is greater than zero
# - Check for the bug which bj sent
# - Add ctrl-shift-alt "Would you like to abort the experiment" message.
# - Fix the thing which takes down puts up a blank screen when the stimulus end.  Maybe not do that or pass a flag.
# - Start timing the stimulus duration after the flip, not before the text is generated.
# - Demo text size bug and submit it to discourse.psychopy and then, conditionally, bug tracker
# - Figure out where this is coming from, might be when we try to calculate mean with no inputs:
#       C:\Program Files (x86)\PsychoPy2\lib\site-packages\numpy\core\fromnumeric.py:2909: RuntimeWarning: Mean of empty slice.
#       out=out, **kwargs)
#       C:\Program Files (x86)\PsychoPy2\lib\site-packages\numpy\core\_methods.py:80: RuntimeWarning: invalid value encountered in double_scalars
#       ret = ret.dtype.type(ret / rcount)






