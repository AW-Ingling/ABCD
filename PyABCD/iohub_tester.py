# iohub_test.py
#
# Kicks the tires on iohub to see if it will work for ABCD.

# REFERENCES:
#
# IOHub keyboard example:
# http://www.isolver-solutions.com/iohubdocs/iohub/quickstart.html
#
# Another IOHub example:
# http://www.psychopy.org/api/iohub/starting.html
#
# Reference tos iohpid error:
# https://github.com/isolver/ioHub/issues/82
# https://groups.google.com/forum/#!topic/psychopy-users/7RRyFl1G7u0
#

# NOTES:
#
# IOHub Error:
# IOError: [Errno 13] Permission denied: 'C:\\Program Files\\JetBrains\\PyCharm Community Edition 2017.2.4\\helpers\\pydev\\.iohpid'
# here:
# iopFile= open(iopFileName,'w')
# "C:\Program Files (x86)\PsychoPy2\lib\site-packages\psychopy\iohub\client\__init__.py", line 990, in _startServer
#


import sys
#from psychopy.iohub import launchHubServer
from psychopy import iohub
#import psychopy


# TODO: These functions are replicated in abcd_show so move them into a common module
def is_keypress(event):
    # String comparison is a workaround for Python claiming that psychopy.iohub.devices.KeyboardPressEventNT does not
    # exist.  We would otherwise use isinstance or issubclass here.
    return str(type(event)) == "<class 'psychopy.iohub.devices.KeyboardPressEventNT'>"

def is_keyrelease(event):
    # String comparison is a workaround for Python claiming that psychopy.iohub.devices.KeyboardPressEventNT does not
    # exist.  We would otherwise use isinstance or issubclass here.
    return str(type(event)) == "<class 'psychopy.iohub.devices.KeyboardReleaseEventNT'>"



io = iohub.launchHubServer()
keyboard = io.devices.keyboard
stop = False
print("Running...")
while not stop:
    for event in keyboard.getEvents():
        print('char: "%s"' % event.char)
        print("modifiers: %s" % str(event.modifiers))
        print("time: %s" % str(event.time))
        print("type: %s" % event.type)
        print("class: %s" % str(type(event)))
        print("key press: %s", is_keypress(event))
        print("key release: %s", is_keyrelease(event))
        print("_______________________________________")
        io.clearEvents()
        if event.key in ['escape', 'q']:
            print("quit key detected")
            stop = True
io.quit()





