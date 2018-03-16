from psychopy import visual, core, gui

w = visual.Window(screen=1, size=(1920,1080), fullscr=False, units='pix')
dlg = gui.Dlg(title=u'FooBar', labelButtonOK=u' Yes ', labelButtonCancel=u' No ', screen=1)
dlg.show()
w.close()