# text_demo.py
#
# experiment with drawing some text to get the ABCD text_display module to work right

# References:
#
# Psychopy TextStim documentation:
# http://www.psychopy.org/api/visual/textstim.html
#
# Psychopy TextStim example
# http://www.psychopy.org/coder/codeStimuli.html
#


from psychopy import visual, core
win = visual.Window(screen=1, fullscr=True, units='pix')
message = visual.TextStim(win, text='Hello \n World')
message.draw()
#message.setAutoDraw(True)  # automatically draw every frame
win.flip()
core.wait(2.0)
message.setText('world')  # change properties of existing stim
message.draw()
win.flip()
core.wait(2.0)

