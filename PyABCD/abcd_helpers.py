# abcd_helpers.py
#
#

# REFERENCES:
#
# find_duplicates() is borrowed and renamed from the JohnLaRooy() function posted on StackOverflow here:
# https://stackoverflow.com/questions/9835762/find-and-list-duplicates-in-a-list/31439372#31439372

import os
import datetime

image_file_extensions = {u'.jpg', u'.png', u'.tiff', u'.tif', u'.gif', u'.bmp'}

table_file_extensions = {u'.xls'}

text_file_extensions = {u'.txt'}

json_file_extensions = {u'.json'}


def is_image_file(filename):
    return os.path.splitext(filename)[1].lower() in image_file_extensions


def is_table_file(filename):
    return os.path.splitext(filename)[1].lower() in table_file_extensions


def is_text_display_file_name(filename):
    return os.path.splitext(filename)[1].lower() in text_file_extensions


def is_text_json_file_name(filename):
    return os.path.splitext(filename)[1].lower() in json_file_extensions


def find_duplicates(a_list):
    seen = set()
    seen2 = set()
    seen_add = seen.add
    seen2_add = seen2.add
    for item in a_list:
        if item in seen:
            seen2_add(item)
        else:
            seen_add(item)
    return list(seen2)


def secs_to_msecs(time_secs):
    if time_secs is None:
        return 0
    else:
        return int(round(time_secs * 1000))


# example return values: "01-22-2018", "07:25:50 PM"
def formatted_date_time():
    now_date_time = datetime.datetime.now()
    now_date_text= now_date_time.strftime("%m-%d-%Y")
    now_time_text= now_date_time.strftime("%I:%M:%S %p")
    return now_date_text, now_time_text


# generates contents of columns "LoseBig", "LoseSmall", "Neutral"
def condition_column_value(column_name, task_name, subtrial_index):
    if column_name == task_name:
        return subtrial_index + 1
    else:
        return "NULL"


# accepts the prbcc flag and returns a value for the "Probe.RESP" column in the output data table
def probe_resp_value(prbacc_flag):
    if prbacc_flag:
        return "{SPACE}"
    else:
        return ""


# accepts a loop counter value 1-n and returns a string for the data output table "BlockTitle" column
def counter_to_block_title(counter):
    return "PracRun_" + str(counter)


# generates the list of differences of successive elements in a list
def succ_diff(num_list):
    return [t - s for s, t in zip(num_list, num_list[1:])]


def paste_int_column():
    column_str = raw_input("Paste a spreadsheet column:")
    column_str_lst = column_str.split()
    column_vals = [int(item) for item in column_str_lst]
    return column_vals


def invert_digit_bool(bool_digit):
    if bool_digit:
        return 0
    else:
        return 1












