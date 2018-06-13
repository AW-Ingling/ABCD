# mid_dialogs.py
#
# Displays dialogs for operator at beginning and end of the MID experiments
#
#
#

from psychopy import gui
from abcd_versions import *
from abcd_recnames import *

dialogs_screen_num = 0


class AskSubjectID:

    #TODO: find out and implement what limits the E-Prime version places on inputs values.

    def __init__(self):
        pass

    def show_input_dialog(self):
        subject_id = "AANNNAAA"
        dlg = gui.Dlg(title=u'E-Run', labelButtonOK=u' OK ', labelButtonCancel=u' Cancel ', screen=dialogs_screen_num)
        dlg.addField("Please Enter the SubjectID", subject_id)
        raw_input = dlg.show()
        if dlg.OK:
            return raw_input[0]
        else:
            return None

    def check_input(self, input_id):
        if len(input_id) > 8:
            dlg = gui.Dlg(title=u'E-Run', labelButtonOK=u' OK ', screen=dialogs_screen_num)
            dlg.addText("Subject ID must be not be longer than 8 characters")
            dlg.show()
            return False
        return True

    def run(self):
        while True:
            input_id = self.show_input_dialog()
            if input_id is not None:
                input_ok = self.check_input(input_id)
                if input_ok:
                    return {'subject_id':input_id}
            else:
                return None


class AskSessionNumber:

    def __init__(self):
        pass

    def show_input_dialog(self):
        input_dlg = gui.Dlg(title=u'E-Run',
                            labelButtonOK=u' OK ',
                            labelButtonCancel=u' Cancel ',
                            screen=dialogs_screen_num)
        input_dlg.addField("Please enter the Session Number (0-32767)", 1)
        raw_input_data = input_dlg.show()
        if input_dlg.OK:
            return raw_input_data[0]
        else:
            return None

    def check_input(self, input_value):
        be_dlg = gui.Dlg(title=u'E-Run', labelButtonOK=u' OK ', screen=dialogs_screen_num)
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


class AskTrialOrderVersion:

    def __init__(self):
        pass

    def show_input_dialog(self):
        input_dlg = gui.Dlg(title=u'E-Run',
                            labelButtonOK=u' OK ',
                            labelButtonCancel=u' Cancel ',
                            screen=dialogs_screen_num)
        input_dlg.addField("Please enter trial order version (1-12)", 1)
        raw_input_data = input_dlg.show()
        if input_dlg.OK:
            return raw_input_data[0]
        else:
            return None

    def check_input(self, input_value):
        be_dlg = gui.Dlg(title=u'E-Run', labelButtonOK=u' OK ', screen=dialogs_screen_num)
        is_error = False
        if type(input_value) is not int and type(input_value) is not long:
            be_dlg.addText("Please enter an integer value")
            is_error = True
        elif input_value < 1:
            be_dlg.addText("The value for Session must not be less than than 1")
            is_error = True
        elif input_value > 12:
            be_dlg.addText("The session value must not be greater than 12")
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
            return {"trial_order_version": input_data}
        else:
            return None


class AskAverageRT:

    def __init__(self):
        pass

    def show_input_dialog(self):
        input_dlg = gui.Dlg(title=u'E-Run',
                            labelButtonOK=u' OK ',
                            labelButtonCancel=u' Cancel ',
                            screen=dialogs_screen_num)
        input_dlg.addField("Please enter the Subject's average RT from the practice run:", 205)
        raw_input_data = input_dlg.show()
        if input_dlg.OK:
            return raw_input_data[0]
        else:
            return None

    def check_input(self, input_value):
        be_dlg = gui.Dlg(title=u'E-Run', labelButtonOK=u' OK ', screen=dialogs_screen_num)
        is_error = False
        if type(input_value) is not int and type(input_value) is not long:
            be_dlg.addText("Please enter an integer value")
            is_error = True
        elif input_value < 0:
            be_dlg.addText("The value for Session must not be less than than 0")
            is_error = True
        elif input_value > 700:
            be_dlg.addText("The session value must not be greater than 700")
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
            return {"average_rt": input_data}
        else:
            return None


class AskHandedness:

    def __init__(self):
        self.dlg = gui.Dlg(title=u'E-Run',
                           labelButtonOK=u' OK ',
                           labelButtonCancel=u' Cancel ',
                           screen=dialogs_screen_num)
        self.dlg.addField("Enter Subject's Handedness", choices=["Right", "Left"])

    def run(self):
        input_data = self.dlg.show()
        if self.dlg.OK:
            return {"handedness": input_data[0]}
        else:
            return None


# class WarnExistingFile:
#
#     def __init__(self, file_name):
#         self.dlg = gui.Dlg(title=u'E-Run', labelButtonOK=u' Yes ', labelButtonCancel=u' No ', screen=dialogs_screen_num)
#         self.dlg.addText("The data file and/or recovery file already exists: %s" % file_name)
#         self.dlg.addText("Do you want to overwrite?")
#
#     def run(self):
#         self.dlg.show()
#         return self.dlg.OK


class SummaryPracticeStartup:

    def __init__(self, inputs_table):
        self.dlg = gui.Dlg(title=u'E-Run', labelButtonOK=u' Yes ', labelButtonCancel=u' No ', screen=dialogs_screen_num)
        self.dlg.addText("NARGUID: %s" % inputs_table['subject_id'])
        self.dlg.addText("Session: %s" % inputs_table['session_number'])
        self.dlg.addText("Handedness: %s" % inputs_table['handedness'])
        self.dlg.addText("Continue with above setup info?")

    def run(self):
        self.dlg.show()
        return self.dlg.OK


class CancelOrContinue:
    def __init__(self):
        self.dlg = gui.Dlg(title=u'E-Run',
                           labelButtonOK=u' Continue ',
                           labelButtonCancel=u' Cancel ',
                           screen=dialogs_screen_num)

    def run(self):
        self.dlg.show()
        return self.dlg.OK


class SummaryScannerStartup:

    def __init__(self, inputs_table):
        self.dlg = gui.Dlg(title=u'E-Run', labelButtonOK=u' Yes ', labelButtonCancel=u' No ', screen=dialogs_screen_num)
        self.dlg.addText("NARGUID: %s" % inputs_table['subject_id'])
        self.dlg.addText("Session: %s" % inputs_table['session_number'])
        self.dlg.addText("Handedness: %s" % inputs_table['handedness'])
        self.dlg.addText("Trial Order: %s" % inputs_table['trial_order_version'])
        self.dlg.addText("PracticeRT: %s" % inputs_table['average_rt'])
        self.dlg.addText("Continue with above setup info?")

    def run(self):
        self.dlg.show()
        return self.dlg.OK




# returns a dictionary with the following key-value pairs:
#
# Key String                  TYPE    DESCRIPTION                        EXAMPLES
#
#                    string  identifies the subject             "AANNNAAA"
# session_number              integer identifies the group number?       1
# handedness                  string  handedness of the subject          "left", "right"
# file_name                   string  full file name including extension "ABCD_MID_Practice_20161209-AANNNAAA-1.xls"
# file_name_without_extension string  full file name without extension   "ABCD_MID_Practice_20161209-AANNNAAA-1"
#
def get_mid_practice_inputs(record_filename_maker, screen_number):
    global dialogs_screen_num
    dialogs_screen_num = screen_number
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
        accept = SummaryPracticeStartup(table).run()
        # ask to quit if not accepted
        if not accept:
            do_continue = CancelOrContinue().run()
            if not do_continue:
                return None
        else:
            break

    # make a new filename
    file_name, file_name_without_extension = record_filename_maker(table['subject_id'], table['session_number'])
    table.update({'file_name' : file_name})
    table.update({'file_name_without_extension': file_name_without_extension})
    return table


# returns a dictionary with the following key-value pairs:
#
# Key String                  TYPE    DESCRIPTION                        EXAMPLES
#
# subject_id                  string  identifies the subject             "AANNNAAA"
# session_number              integer identifies the group number?       1
# handedness                  string  handedness of the subject          "left", "right"
# file_name                   string  full file name including extension "ABCD_MID_Practice_20161209-AANNNAAA-1.xls"
# file_name_without_extension string  full file name without extension   "ABCD_MID_Practice_20161209-AANNNAAA-1"
# trial_order_version         integer index of stimulus tables           1
# average_rt                  integer average reaction time of practice  350
def get_mid_scanner_inputs(record_filename_maker, screen_number):
    global dialogs_screen_num
    dialogs_screen_num = screen_number
    while True:
        table = {}
        # get the subject ID #1
        subject_id = AskSubjectID().run()
        if subject_id is None:
            return None
        table.update(subject_id)
        # get the session number #2
        session_number = AskSessionNumber().run()
        if session_number is None:
            return None
        table.update(session_number)
        # get the handedness #3
        handedness = AskHandedness().run()
        if handedness is None:
            return None
        table.update(handedness)
        # get the trial order version #4
        trial_order_version = AskTrialOrderVersion().run()
        if trial_order_version is None:
            return
        table.update(trial_order_version)
        # get the subject's average reaction time from the practice run
        average_rt = AskAverageRT().run()
        if average_rt is None:
            return
        table.update(average_rt)
        # show the summary and query to accept it
        accept = SummaryScannerStartup(table).run()
        # ask to quit if not accepted
        if not accept:
            do_continue = CancelOrContinue().run()
            if not do_continue:
                return None
        else:
            break

    # make a new filename
    file_name, file_name_without_extension = record_filename_maker(table['subject_id'], table['session_number'])
    table.update({'file_name' : file_name})
    table.update({'file_name_without_extension': file_name_without_extension})
    return table
















