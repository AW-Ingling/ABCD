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
import enum
from psychopy import visual, core, monitors
import pyglet
import platform


# define enumerated type for specifying the a of selecting monitor on multi-monitor systems.
class MonitorSearchMethod(enum.Enum):
    SEARCH_BY_SIZE = 1
    SEARCH_BY_INDEX = 2

class MonitorFallbackMethod(enum.Enum):
    FALLBACK_STRICT = 1
    FALLBACK_ACCEPT_ANY_SINGLE = 2
    FALLBACK_TAKE_SECOND = 3
    FALLBACK_MAC_PYGLET_BUG = 4


# Define some parameters as constants
MONITOR_SEARCH_METHOD = MonitorSearchMethod.SEARCH_BY_SIZE
MONITOR_FALLBACK_METHODS = {MonitorFallbackMethod.FALLBACK_TAKE_SECOND,
                            MonitorFallbackMethod.FALLBACK_ACCEPT_ANY_SINGLE}
PREFERRED_SCREEN_RESOLUTION = (1920, 1080)
PREFERRED_SCREEN_INDEX = 1

# Detect if we are on a mac and change the fallback mode to one which only uses the first monitor
if platform.system() == "Darwin":
    print("Detected MacOS, resetting monitor fallback mode to FALLBACK_MAC_PYGLET_BUG.")
    MONITOR_FALLBACK_METHODS = {MonitorFallbackMethod.FALLBACK_MAC_PYGLET_BUG}

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
def find_screens_by_index(index, screens):
    matched_screens = [screen for iter_index, screen in enumerate(screens)  if iter_index == index]
    matched_indices = [iter_index for iter_index, screen in enumerate(screens)  if iter_index == index]
    return matched_screens, matched_indices

# functions for matching screen by index
def find_screens_by_size(size_pixels, screens):
    dims_pixels= [(screen.width, screen.height) for screen in screens]
    matched_screen_indices = [index for index, dims in enumerate(dims_pixels) if dims == size_pixels]
    matched_screens = [screen for index, screen in enumerate(screens) if index in matched_screen_indices]
    return matched_screens, matched_screen_indices


_target_by_index_screens, _target_by_index_screens_indices = find_screens_by_index(PREFERRED_SCREEN_INDEX, all_screens)
_target_by_size_screens, _taget_by_size_screens_indices = find_screens_by_size(PREFERRED_SCREEN_RESOLUTION, all_screens)


# find lists of monitors by index and by size
if MONITOR_SEARCH_METHOD == MonitorSearchMethod.SEARCH_BY_INDEX:
    target_screens = _target_by_index_screens
    target_screens_indices = _target_by_index_screens_indices
elif MONITOR_SEARCH_METHOD == MonitorSearchMethod.SEARCH_BY_SIZE:
    target_screens = _target_by_size_screens
    target_screens_indices = _taget_by_size_screens_indices
else:
    print("ERROR: Unknown monitor search method, exiting.")
    sys.exit()



if len(target_screens) == 1:
    # if we have exactly one exact match between specified monitor and available monitors then return it.
    target_screen = target_screens[0]
    target_screen_index = target_screens_indices[0]
    print("Found monitor matching specifications.")
elif MonitorFallbackMethod.FALLBACK_STRICT in MONITOR_FALLBACK_METHODS and len(target_screens) == 0:
    # if strick match is required and there is no exact match then exit.
    print("ERROR: Failed to find any screens with specified size: %s, exiting" % str(PREFERRED_SCREEN_RESOLUTION))
    # TODO: Put a dialog box warning here, inventory the error.
    sys.exit()
elif MonitorFallbackMethod.FALLBACK_MAC_PYGLET_BUG in MONITOR_FALLBACK_METHODS  and len(all_screens) >= 1:
    # if we are in fallback pyglet mode then alwyas use the 0th display
    target_screen = all_screens[0]
    target_screen_index = 0
elif MonitorFallbackMethod.FALLBACK_ACCEPT_ANY_SINGLE in MONITOR_FALLBACK_METHODS and len(all_screens) == 1:
    # if here is only one connected monitor and fallback says we can use that then do
    target_screen = all_screens[0]
    target_screen_index = 0
    print("Failed to find monitor matching specifications.  Falling back to the single connected display.")
elif MonitorFallbackMethod.FALLBACK_TAKE_SECOND in MONITOR_FALLBACK_METHODS and len(all_screens) > 1:
    # if there are multiple monitors and no exact matches and fallback says to take the secondary display.
    target_screen = all_screens[1]
    target_screen_index = 1
    print("Failed to find monitor matching specifications.  Falling back to second connected display.")


print("Selected monitor at enumeration index %d" % target_screen_index)
print("Selected: %s." % target_screen.get_mode())

#TODO: Implement the case for multiple mismatching sized displays
#TODO: Implement the case for permissive matching but no matching name.  Fallback to size?

#TODO We assume here that Pyglet indexes monitors in the same order as PsychoPy.  Check that assumption and test.
#TODO Check if the primary monitor is always enumerated first.
#TODO Check if the enumeration order matches the order in the Windows displays panel

#TODO Refactor all of this into a class

def get_target_screen_index():
    return target_screen_index

def open_stimulus_window():
    global stimulus_window
    stimulus_window = visual.Window(screen=target_screen_index, fullscr=True, units='pix')
    return stimulus_window

def close_stimulus_window():
    stimulus_window.close()





















