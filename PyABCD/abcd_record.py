# abcd_record.py
#
# Stores data from a session and dumps it to a spreadsheet, replicating the E-Prime edat2 files

# Resources:
#
# For converting between spreadsheet coordinates and cell indices:
# See:
#   https://stackoverflow.com/questions/19415937/python-xlwt-convert-column-integer-into-excel-cell-references-eg-3-6-to-c6
#   http://nullege.com/codes/search/xlwt.Utils.cell_to_rowcol
# Examples:
#   xlwt.Utils.col_by_name("B")
#   xlwt.Utils.cell_to_rowcol("B2")
#   num_index = xlwt.Utils.col_by_name(letter_index)
#

import os
import string
import itertools
import xlwt


class ConstantColumn(object):

    def __init__(self, num_index, value):
        self.num_index = num_index
        self.value = value


class ColumnLabel(object):

    @classmethod
    def labels_from_text(cls, text_list):
        return [ColumnLabel(index, text) for index, text in enumerate(text_list)]

    @classmethod
    def draw_labels_in_sheet(cls, sheet, column_labels, row_num_index):
        for column_label in column_labels:
            column_label.draw_label_in_sheet(sheet, row_num_index)
        return row_num_index + 1

    def __init__(self, column_num_index, text):
        self.column_number_index = column_num_index
        self.text = text
        self.row_num_index = None

    def draw_label_in_sheet(self, sheet, row_num_index):
        self.row_num_index = row_num_index
        sheet_row = sheet.row(row_num_index)
        sheet_row.write(self.column_number_index, self.text)


class AbcdRow(object):

    def __init__(self, row_num_index, total_columns):
        self.row_num_index = row_num_index
        self.total_column = total_columns
        self.contents = ["" for index in range(0, total_columns)]

    def draw_row_in_sheet(self, sheet):
        sheet_row = sheet.row(self.row_num_index)
        for index, content in enumerate(self.contents):
            sheet_row.write(index, content)

    def add_cell(self, column_num_index, value):
        #column_num_index= xlwt.Utils.col_by_name(column_letter_index)
        self.contents[column_num_index] = value

    def add_constant_columns(self, constant_columns):
        for constant_column in constant_columns:
            self.add_cell(constant_column.num_index, constant_column.value)


class AbcdRecord(object):

    def __init__(self, output_dir_path, file_name, column_labels_text):
        # construct full write path
        self.full_file_name = file_name
        self.full_path = os.path.join(output_dir_path, self.full_file_name)
        print("path to file: %s" % self.full_path)
        # we never over-write existing files, so make sure that it does not exit.
        if os.path.isfile(self.full_path):
            raise Exception("Output record file already exists")
        # init state/retain ags
        self.columns_labels_text = column_labels_text
        self.constant_columns = []
        self.column_labels = None
        self.current_row_index = 0
        self.current_row = None
        self.width_columns = len(column_labels_text)
        self.rows = []
        # create spreadsheet
        self.workbook = xlwt.Workbook()
        self.worksheet = self.workbook.add_sheet("Sheet 1")
        # draw column labels into worksheet
        self.draw_column_labels()

    def draw_column_labels(self):
        self.column_labels = ColumnLabel.labels_from_text(self.columns_labels_text)
        self.current_row_index = ColumnLabel.draw_labels_in_sheet(self.worksheet, self.column_labels, self.current_row_index)

    def column_index_for_label(self, label_text):
        return self.columns_labels_text.index(label_text)

    def add_constant_column(self, label_text, value):
        column_num_index = self.column_index_for_label(label_text)
        self.constant_columns.append(ConstantColumn(column_num_index, value))

    def add_batch_constant_columns(self, label_value_table):
        for label_value_pair in label_value_table:
            self.add_constant_column(label_value_pair[0], label_value_pair[1])

    def add_new_row(self):
        self.current_row = AbcdRow(self.current_row_index, self.width_columns)
        self.rows.append(self.current_row)
        self.current_row_index += 1

    def add_cell_value_to_row(self, label, value):
        column_index = self.column_index_for_label(label)
        self.current_row.add_cell(column_index, value)

    def add_cell_value_to_columns(self, labels, value):
        for label in labels:
            self.add_cell_value_to_row(label, value)

    def fill_column_data(self, label, value):
        column_index = self.column_index_for_label(label)
        for row in self.rows:
            row.add_cell(column_index, value)

    def save(self):
        for row in self.rows:
            row.add_constant_columns(self.constant_columns)
            row.draw_row_in_sheet(self.worksheet)
        # write the spreadsheet
        self.workbook.save(self.full_path)









