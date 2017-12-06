
# REFERENCES:
# IOHub example:
# http://www.isolver-solutions.com/iohubdocs/iohub/quickstart.html

import sys
#from psychopy.iohub import launchHubServer
from psychopy import iohub
#import psychopy


def keyboard_event_type_name_for_event(event):
    event_name = ""
    if isinstance(event, iohub.devices.KeyboardPressEventNT):
        event_name = "press"
    elif issubclass(event, iohub.devices.KeyboardReleaseEventNT):
        event_name = "release"
    else:
        print("Warning: unrecognized keyboard event type:")
    print("\t%s." % str(type(event)))
    return event_name


io = iohub.launchHubServer()
keyboard = io.devices.keyboard
events = keyboard.getEvents()
keys = [event.key for event in events]
print(keys)
stop = False
print("Running...")
while not stop:
    for event in keyboard.getEvents():
        print('char: "%s"' % event.char)
        print("modifiers: %s" % str(event.modifiers))
        print("time: %s" % str(event.time))
        print("type: %s" % event.type)
        print("class: %s" % keyboard_event_type_name_for_event(event))
        print("_______________________________________")
        io.clearEvents()
        if event.key in ['escape', 'q']:
            print("quit key detected")
            stop = True






