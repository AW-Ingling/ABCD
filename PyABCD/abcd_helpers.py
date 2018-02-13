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













