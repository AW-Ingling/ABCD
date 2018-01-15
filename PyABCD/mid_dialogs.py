# mid_dialogs.py
#
# Displays dialogs for operator at beginning and end of the MID experiments

from psychopy import gui

class AskSubjectID:

    #TODO: find out and implement what limits the E-Prime version places on inputs values.

    def __init__(self):
        subject_id = "AANNNAAA"
        self.dlg = gui.Dlg(title=u'E-Run', labelButtonOK=u' OK ', labelButtonCancel=u' Cancel ')
        self.dlg.addField("Please Enter the SubjectID", subject_id)

    def run(self):
        input_data = self.dlg.show()
        if self.dlg.OK:
            return {"subject_id": input_data[0]}
        else:
            return None


class AskSessionNumber:

    def __init__(self):
        pass

    def show_input_dialog(self):
        input_dlg = gui.Dlg(title=u'E-Run', labelButtonOK=u' OK ', labelButtonCancel=u' Cancel ')
        input_dlg.addField("Please enter the Session Number (0-32767)", 1)
        raw_input_data = input_dlg.show()
        if input_dlg.OK:
            return raw_input_data[0]
        else:
            return None

    def check_input(self, input_value):
        be_dlg = gui.Dlg(title=u'E-Run', labelButtonOK=u' OK ')
        is_error = False
        if type(input_value) is not int and type(input_value) is not long:
            be_dlg.addText("Please enter an integer value")
            is_error = True
        elif input_value < 0:
            be_dlg.addText("The value for Session must not be less than than 0")
            is_error = True
        elif input_value > 32767:
            be_dlg.addText("The session value must not be greater than 32767")
            is_error = True
        if is_error:
            be_dlg.show()
        return is_error

    def run(self):
        no_input = True
        while no_input:
            input_data = self.show_input_dialog()
            if input_data is not None:
                no_input = self.check_input(input_data)
            else:
                no_input = False
        if input_data:
            return {"session_number": input_data}
        else:
            return None


class AskHandedness:

    def __init__(self):
        self.dlg = gui.Dlg(title=u'E-Run', labelButtonOK=u' OK ', labelButtonCancel=u' Cancel ')
        self.dlg.addField("Enter Subject's Handedness", choices=["Right", "Left"])

    def run(self):
        input_data = self.dlg.show()
        if self.dlg.OK:
            return {"handedness": input_data[0]}
        else:
            return None







