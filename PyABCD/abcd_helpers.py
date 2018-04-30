# abcd_helpers.py
#
#

# REFERENCES:
#
# find_duplicates() is borrowed and renamed from the JohnLaRooy() function posted on StackOverflow here:
# https://stackoverflow.com/questions/9835762/find-and-list-duplicates-in-a-list/31439372#31439372
#
# how to exclude leading zeros on date formatters:
# https://stackoverflow.com/questions/904928/python-strftime-date-without-leading-0
#
# date formatter keys:
# https://docs.python.org/2/library/time.html#time.strftime
#
# how to convert a time between time zones:
# https://stackoverflow.com/questions/4770297/convert-utc-datetime-string-to-local-datetime-with-python
#

import os
import platform
import datetime
from dateutil import tz


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

def msecs_to_secs(time_msecs):
    return  time_msecs / 1000.0


# # example return values: "01-22-2018", "07:25:50 PM"
# def formatted_date_time():
#     now_date_time = datetime.datetime.now()
#     now_date_text= now_date_time.strftime("%m-%d-%Y")
#     now_time_text= now_date_time.strftime("%I:%M:%S %p")
#
#     return now_date_text, now_time_text

# example return values: "01-22-2018",  "2/21/2018 8:03:40 PM"   "07:25:50 PM",  <-- we probably need to fix this
#   more example values: "02-21-2018"	"2/21/2018 8:03:40 PM"	 "15:03:40"      <-- from export, not spreadsheet
def formatted_date_time():

    utc_zone = tz.tzutc()
    local_zone = tz.tzlocal()
    utc_date_time = datetime.datetime.utcnow()
    utc_date_time = utc_date_time.replace(tzinfo=utc_zone)
    local_date_time = utc_date_time.astimezone(local_zone)
    local_date_text= local_date_time.strftime("%m-%d-%Y")
    local_time_text= local_date_time.strftime("%H:%M:%S")
    if platform.system() == "Windows":  # - uses a "#" to exclude leading zero on field
        datetime_formatter = "%#m/%#d/%Y %#I:%M:%S %p"
    else: # "Linux", "Darwin" - uses a "-" to exclude leading zero on field
        datetime_formatter = "%-m/%-d/%Y %-I:%M:%S %p"
    date_time_utc_text = utc_date_time.strftime(datetime_formatter)
    return local_date_text, date_time_utc_text, local_time_text


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












