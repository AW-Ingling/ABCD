# abcd_helpers.py
#
#

# REFERENCES:
#
# find_duplicates() is borrowed and renamed from the JohnLaRooy() function posted on StackOverflow here:
# https://stackoverflow.com/questions/9835762/find-and-list-duplicates-in-a-list/31439372#31439372

import os

image_file_extensions = {u'.jpg', u'.png', u'.tiff', u'.tif', u'.gif', u'.bmp'}

table_file_extensions = {u'.xls'}


def is_image_file(filename):
    return os.path.splitext(filename)[1].lower() in image_file_extensions


def is_table_file(filename):
    return os.path.splitext(filename)[1].lower() in table_file_extensions


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











