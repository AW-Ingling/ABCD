

time_version_filename_prefix = "TimeVersion"

trial_order_table = dict()

trial_order_table[1] = {1: 5,
                        2: 13,
                        3: 9,
                        4: 15,
                        5: 6,
                        6: 8,
                        7: 2,
                        8: 3,
                        9: 10,
                        10: 7,
                        11: 11,
                        12: 4}

trial_order_table[2] = {1: 16,
                        2: 1,
                        3: 14,
                        4: 12,
                        5: 5,
                        6: 11,
                        7: 9,
                        8: 8,
                        9: 2,
                        10: 13,
                        11: 7,
                        12: 3}

def time_version_file_name(r_number, trial_order):
    file_number = trial_order_table[r_number][trial_order]
    file_name = time_version_filename_prefix + str(file_number)
    return file_name






