
# TODO

#
# - Create a git release branch and re-direct BJ to that
# - Create a github issue tracker for the project
# - Create Run two passes through the second test loop to see what happens the null line, then move the null line generator accordingly.
# - Find out if we
# - Add instructions to use pythonw instead of python
# - Figure out what is going on with openining a fullscreen window on the second screen in PsychoPy on OS X.
# - Figure out what is going on with the the first test sequence which seems to mis-detect kepresses on OS X.
# - Add a note to enable assistive devices on OS X
# - Add the path to the interpreter in MacOS:
#   import os
#   os.environ
#   export PYTHONHOME=/Applications/PsychoPy2.app/Contents/Resources
# - the "ProbeDuration" column is missing in the output spreadsheet sample and Python data output table
# - check for other missing columns
# - check if we need to invert the loop nesting for the first practice sequence, seems to be the wrong order.
# - test this line in mid_practice:
#   tbl_condition = run_list_table.cell_value("Condition", run_list_index + 1)
# - Verify that the session number is the same as the group number.
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
#
#






