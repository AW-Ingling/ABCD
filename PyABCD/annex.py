# annex.py
#
#  Various stuff cut out of development code which we might eventually want but is cluttering up the running code


import itertools
import string


def letter_index_to_column_index(letter_index):
    cindex = 0
    for index, letter in enumerate(letter_index[::-1]):
        cindex +=  26**index * (string.lowercase.index(letter.lower()) + 1)
    return cindex


# Make a list of pairs of index, letter_combination where index is the lexicographic index of the
# letter string according to our column numbering scheme defined by letter_index_to_column_index().
# used to test letter_index_to_column_index
def make_test_index_letter_pairs(num_letter_digits):
    letter_combs = itertools.product(string.ascii_lowercase, repeat=num_letter_digits)
    pairs = [(index, "".join(letter_comb)) for index, letter_comb in enumerate(letter_combs)]
    return pairs

# NOTE: this is not quite right because we need to offset the indices by all lower num_alpha_digits length lists.
#
def test_litcoi(num_alpha_digits):
    test_set = make_test_index_letter_pairs(num_alpha_digits)
    for index_and_alpha_num in test_set:
        calculated_index = letter_index_to_column_index(index_and_alpha_num[1])