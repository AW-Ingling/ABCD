# hm_tester.py
#
# Try to find a way to hide the mouse pointer; The obvious way, to set window.mouseVisible = False, only works after
# clicking once inside the fullscreen window when two monitors are connected.
#
# REFERENCES:
#
# Custom Mouse:
# https://groups.google.com/forum/#!topic/psychopy-users/ZZkM82GzUic
# http://www.psychopy.org/api/visual/custommouse.html
#
#

# Things to try:
# - Simulate a mouse click
# - Hide the mouse using CustomMouse.
# - Use CustomMouse to create and invisible mouse.
# - Bound the mouse off the lower-right corner of the screen
# - Bound the mouse onto the other screen
# - Use another API (Pyglet)

from psychopy import visual, core, event, iohub
import pyglet

# works until the operator clicks outside of the fullscreen window
def t1():
    w = visual.Window(screen=1, fullscr=True, units='pix')
    m = visual.CustomMouse(w, visible=False)
    t_end = core.getTime() + 20
    while core.getTime() < t_end:
        m.draw()
        core.wait(0.010)
    w.close()


def t2():
    w = visual.Window(screen=1, fullscr=True, units='pix')
    m = visual.CustomMouse(w, visible=False, leftLimit = 1900, topLimit = 20)
    t_end = core.getTime() + 20
    while core.getTime() < t_end:
        m.draw()
        core.wait(0.010)
    w.close()

def t3():
    platform = pyglet.window.get_platform()
    display = platform.get_default_display()
    screens = display.get_screens()
    w = pyglet.window.Window(fullscreen=True, screen=screens[1])
    w.set_exclusive_mouse(True)
    pyglet.app.run()

# This one works.
def t4():
    w = visual.Window(screen=1, fullscr=True, units='pix')
    m = event.Mouse(visible=False, win=w)
    m.setExclusive(True)
    t_end = core.getTime() + 10
    while core.getTime() < t_end:
        core.wait(0.010)
    m.setExclusive(False)
    w.close()


def t5():
    # Open the window and hide the cursor
    w = visual.Window(screen=1, fullscr=True, units='pix')
    m = event.Mouse(visible=False, win=w)
    m.setExclusive(True)

    # Turn on IOHub
    io = iohub.launchHubServer()
    kb = io.devices.keyboard

    # Delay a while
    t_end = core.getTime() + 10
    while core.getTime() < t_end:
        core.wait(0.010)

    # Turn off iohub, release the cursor and close the window
    io.quit()
    m.setExclusive(False)
    w.close()



