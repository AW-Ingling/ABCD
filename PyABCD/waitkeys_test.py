# waitkeys_test.py
#
# Demonstrates that waitKeys requires an opened window in focus and that it also requires window focus.  The latter
# makes it unsuitable for the ABCD tasks; Should the operator accidentally change focus, that breaks input collection
# from the subject.


from psychopy import visual
from psychopy import event

w = visual.Window(screen=0)
ks=event.waitKeys()
w.close()
print("Keys: %s" % str(ks))

