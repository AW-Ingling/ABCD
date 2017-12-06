# test_vis.py
#
# Tries out Python 2.7 with Psychopy on Windows 10

# TODO: Make sure that Pyglet's enumerution of screens matches Psychopy's
# TODO: Detect and warn if Psychopy is using Pygame instead of Pyglet, see above
# TODO: Retest the screen finder with more than one screen.
# TODO: Check if the naming scheme in the Windows display gui match Pyglet naming
# TODO: Enumerate all errors

# Major To Dos:
# Refactor this into a class


# Imports
import sys
from psychopy import visual, core, monitors
import pyglet
import enum


# define enumerated type for specifying the a of selecting monitor on multi-monitor systems.
class MonitorSearchMethod(enum.Enum):
    SEARCH_BY_SIZE = 1
    SEARCH_BY_NAME = 2

class MonitorFallbackMethod(enum.Enum):
    FALLBACK_STRICT = 1
    FALLBACK_ACCEPT_ANY_SINGLE = 2


# Define some parameters as constants
MONITOR_SEARCH_METHOD = MonitorSearchMethod.SEARCH_BY_SIZE
MONITOR_FALLBACK_METHOD = MonitorFallbackMethod.FALLBACK_ACCEPT_ANY_SINGLE
PREFERRED_SCREEN_RESOLUTION = (1920, 1080)
PREFERRED_SCREEN_NAME = u'DISPLAY1'

# Default Stimulus Window
stimulus_window = None

# Get the list of all screens from Pyglet
print("Getting list of all screens...")
_platform = pyglet.window.get_platform()
_display = _platform.get_default_display()
all_screens = _display.get_screens()
print("Detected %d screens:" % len(all_screens))
for index, screen in enumerate(all_screens):
    print("\t%d: %s" % (index, screen.get_mode()))

# Functions for matching screen resolution
def find_screens_by_size(size_pixels, screens):
    dims_pixels= [(screen.width, screen.height) for screen in screens]
    matched_screen_indices = [index for index, dims in enumerate(dims_pixels) if dims == size_pixels]
    matched_screens = [screen for index, screen in enumerate(screens) if index in matched_screen_indices]
    return matched_screens, matched_screen_indices

def find_screens_by_name(name, screens):
    names = [screen.get_device_name() for screen in screens]
    matched_name_indices = [index for index, name in enumerate(names) if PREFERRED_SCREEN_NAME.upper() in name.upper()]
    matched_screens = [screen for index, screen in enumerate(screens) if index in matched_name_indices]
    return matched_screens, matched_name_indices

# Select the display; The experiment expects a 1920x1080 display, so find displays of that size
print("Looking for screens with dimensions %s..." % str(PREFERRED_SCREEN_RESOLUTION))
_target_size_screens, _taget_size_screens_indices = find_screens_by_size(PREFERRED_SCREEN_RESOLUTION, all_screens)

# Select the display; The experiment expects a 1920x1080 display, so find displays of that size
print("Looking for screen named %s..." % PREFERRED_SCREEN_NAME)
_target_name_screens, _target_name_screens_indices = find_screens_by_name(PREFERRED_SCREEN_NAME, all_screens)


# If name search is specified, use the list of monitors with matching names.
# If size search is specified, use the list of monitors with matching sizes
if MONITOR_SEARCH_METHOD == MonitorSearchMethod.SEARCH_BY_NAME:
    target_screens = _target_name_screens
    target_screens_indices = _target_name_screens_indices
    print(u'Selecting screen by preferred name: %s.' % PREFERRED_SCREEN_NAME)
elif MONITOR_SEARCH_METHOD == MonitorSearchMethod.SEARCH_BY_SIZE:
    target_screens = _target_size_screens
    target_screens_indices = _taget_size_screens_indices
    print(u'Selecting screen by preferred dimensions: %s.' % str(PREFERRED_SCREEN_RESOLUTION))
else:
    print("ERROR: Unknown monitor search method, exiting.")
    sys.exit()

if len(target_screens) == 1:
    target_screen = target_screens[0]
    target_screen_index = target_screens_indices[0]
    print("Found monitor matching specifications.")
elif MONITOR_FALLBACK_METHOD == MonitorFallbackMethod.FALLBACK_ACCEPT_ANY_SINGLE and len(all_screens) == 1:
    target_screen = all_screens[0]
    target_screen_index = 0
    print("Failed to find monitor matching specifications.  Falling back to the single connected display.")
elif MONITOR_FALLBACK_METHOD == MonitorFallbackMethod.FALLBACK_STRICT and len(target_screens) == 0:
    print("ERROR: Failed to find any screens with specified size: %s, exiting" % str(PREFERRED_SCREEN_RESOLUTION))
    #TODO: Put a dialog box warning here, inventory the error.
    sys.exit()

print("Selected monitor at enumeration index %d" % target_screen_index)
print("Selected: %s." % target_screen.get_mode())

#TODO: Implement the case for multiple mismatching sized displays
#TODO: Implement the case for permissive matching but no matching name.  Fallback to size?

#TODO We assume here that Pyglet indexes monitors in the same order as PsychoPy.  Check that assumption and test.
#TODO Check if the primary monitor is always enumerated first.
#TODO Check if the enumeration order matches the order in the Windows displays panel

#TODO Refactor all of this into a class

def open_stimulus_window():
    global stimulus_window
    stimulus_window = visual.Window(screen=target_screen_index, fullscr=True)

def close_stimulus_window():
    stimulus_window.close()





















