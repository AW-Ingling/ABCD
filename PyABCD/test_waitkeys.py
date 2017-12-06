# test_waitkeys
#
# Demonstrates that waitKeys requires an opened window in focus.


from psychopy import visual
from psychopy import event

w = visual.Window(screen=0)
ks=event.waitKeys()
w.close()
print("Keys: %s" % str(ks))

