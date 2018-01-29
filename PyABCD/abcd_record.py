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
#
#

import os
import string
import itertools
import xlwt


class ConstantColumn:

    def __init__(self, letter_index, value):
        self.letter_index = letter_index
        self.value = value
        self.column_index = xlwt.Utils.col_by_name(letter_index)


class ColumnLabel:

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


class AbcdRecord:

    def __init__(self, output_dir_path, file_name, column_labels_text):
        # construct full write path
        self.full_file_name = file_name + ".xls"
        self.full_path = os.path.join(output_dir_path, self.full_file_name)
        print("path to file: %s" % self.full_path)
        # init state/retain ags
        self.columns_labels_text = column_labels_text
        self.constant_fields = []
        self.column_labels = None
        self.current_row = 0
        # create spreadsheet
        self.workbook = xlwt.Workbook()
        self.worksheet = self.workbook.add_sheet("Sheet 1")
        # draw column labels into worksheet
        self.draw_column_labels()

    def draw_column_labels(self):
        self.column_labels = ColumnLabel.labels_from_text(self.columns_labels_text)
        self.current_row = ColumnLabel.draw_labels_in_sheet(self.worksheet, self.column_labels, self.current_row)

    def add_constant_field(self, letter_index, value):
        self.constant_fields.append(ConstantColumn(letter_index, value))

    def save(self):
        self.workbook.save(self.full_path)







