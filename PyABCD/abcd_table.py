# abcd_table.py
#
# Loads Excel format files which hold stimulus tables copied from E-Prime ABCD scripts.
# Equivalent of the E-Prime "list" component.

# REFERENCES:
#
# How to find empty lines in excel which we use to identify data table bounds
# https://stackoverflow.com/questions/42843830/how-to-stop-reading-a-spreadsheet-with-xlrd-at-the-first-empty-row

import os
import sys
import xlrd
import stim_bundle

class AbcdTable:

    def __init__(self, stim_bundle, table_name):
        # drill down from the file name to get the sheet object
        self.table_name = table_name
        self.excel_file_path = stim_bundle.excel_file_path_for_table_name(table_name)
        book = xlrd.open_workbook(self.excel_file_path)
        self.sheet = book.sheet_by_index(0)
        # declare instance variables set elsewhere, in load_sheet()
        self.label_row_index = None
        self.first_data_row_index = None
        self.last_data_row_index = None
        self.num_rows = 0
        self.field_map = {}
        self.table = {}
        # load contents of sheet into our native data table
        self.load_table_from_sheet()
        #TODO: Detect Additional sheets and warn because we expect one per workbook (aka file)

    def load_table_from_sheet(self):
        # find row index of the column header row which should be the first non-emtpy row in the table
        self.label_row_index = self.find_next_data_row(0)
        # find the index of the first data row which is the first non-empty row after the column header row
        self.first_data_row_index = self.find_next_data_row(self.label_row_index + 1)
        # find the final data row index which is the first non-empty row up from the bottom of the table
        self.last_data_row_index = self.find_last_data_row()
        # make a table mapping column name to column index
        self.field_map = self.read_field_map()
        # build a table of empty lists so we can use append when associating elements with name indices
        for column_name in self.field_map:
            self.table[column_name] = []
        # iterate down each row adding elements to each name index's list
        for column_name in self.field_map:
            steps = range(self.first_data_row_index, self.last_data_row_index+1)
            self.num_rows = len(steps)
            for row in steps:
                self.table[column_name].append(self.sheet.cell(row, self.field_map[column_name]).value)

    def is_empty_cell(self, row_index , column_index):
        cell_value = self.sheet.cell(row_index, column_index).value
        return str(cell_value).strip() == ''

    def is_empty_row(self, row_index):
        for column in range(0, self.sheet.ncols):
            if not self.is_empty_cell(row_index, column):
                return False
        return True

    def find_next_data_row(self, from_row_index):
        for row_index in range(from_row_index, self.sheet.nrows):
            if not self.is_empty_row(row_index):
                return row_index
        return None

    def find_last_data_row(self):
        for row in range(0, self.sheet.nrows)[::-1]:
            if not self.is_empty_row(row):
                return row
        return None

    def read_field_map(self):
        field_map = {}
        for column in range(0, self.sheet.ncols):
            if not self.is_empty_cell(self.label_row_index, column):
                field_map[self.sheet.cell(self.label_row_index, column).value] = column
        return field_map

    @property
    def column_names(self):
        return self.table.keys()

    def print_column(self, column_name):
        for value in self.table[column_name]:
            print("%s" % str(value))

    def __str__(self):
        txt = ""
        for key in self.table:
            txt += "\n%s\n" % str(key)
            for value in self.table[key]:
                txt += "\t%s\n" % value
        return txt

    # TODO: change this to 0-index from 1-index.
    def cell_value(self, column_name, row_id):
        # Find the row index of the specified row_id in the table's "ID" column
        indices_of_id = [index for index, value in enumerate(self.table["ID"]) if value == row_id]
        if len(indices_of_id) < 1:
            msg = "Error: Unrecognized table cell row id for table: %s, column: %s, row id: %s\n" % \
                 (self.table_name, column_name, str(row_id))
            raise Exception(msg)
        if len(indices_of_id) < 1:
            msg = "Error: Multiple table cell row ids for table: %s, column: %s, row id: %s\n" % \
                 (self.table_name, column_name, str(row_id))
            raise Exception(msg)
        # Return the item at the specified row_id's row index and in the specified column
        return self.table[column_name][indices_of_id[0]]






















