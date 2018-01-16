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
            return {"subject_id": str(input_data[0])}
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


class WarnExistingFile:

    def __init__(self, file_name):
        self.dlg = gui.Dlg(title=u'E-Run', labelButtonOK=u' Yes ', labelButtonCancel=u' No ')
        self.dlg.addText("The data file and/or recovery file already exists: %s" % file_name)
        self.dlg.addText("Do you want to overwrite?")

    def run(self):
        self.dlg.show()
        return self.dlg.OK


class SummaryStartup:

    def __init__(self, inputs_table):
        self.dlg = gui.Dlg(title=u'E-Run', labelButtonOK=u' Yes ', labelButtonCancel=u' No ')
        self.dlg.addText("NARGUID: %s" % inputs_table['subject_id'])
        self.dlg.addText("Session: %s" % inputs_table['session_number'])
        self.dlg.addText("Handedness: %s" % inputs_table['handedness'])
        self.dlg.addText("Continue with above setup info?")

    def run(self):
        self.dlg.show()
        return self.dlg.OK


class CancelOrContinue:
    def __init__(self):
        self.dlg = gui.Dlg(title=u'E-Run', labelButtonOK=u' Continue ', labelButtonCancel=u' Cancel ')

    def run(self):
        self.dlg.show()
        return self.dlg.OK


def get_inputs(file_exists_checker):
    while True:
        table = {}
        # get the subject ID
        subject_id = AskSubjectID().run()
        if subject_id is None:
            return None
        table.update(subject_id)
        # get the session number
        session_number = AskSessionNumber().run()
        if session_number is None:
            return None
        table.update(session_number)
        # get the handedness
        handedness = AskHandedness().run()
        if handedness is None:
            return None
        table.update(handedness)
        # show the summary and query to accept it
        accept = SummaryStartup(table).run()
        # ask to quit if not accepted
        if not accept:
            do_continue = CancelOrContinue().run()
            if not do_continue:
                return None
        else:
            break
    # check if the file already exists and warn accordingly
    exists, file_name = file_exists_checker(table['subject_id'], table['session_number'])
    table.update({'file_name' : file_name})
    if exists:
        do_overwrite = WarnExistingFile(file_name).run()
        if do_overwrite:
            return table
        else:
            return None
    return table


def yes_file_exists_dummy(subject_id, session_number):
    return True, subject_id + "_" + str(session_number)


def no_file_exists_dummy(subject_id, session_number):
    return False, subject_id + "_" + str(session_number)















