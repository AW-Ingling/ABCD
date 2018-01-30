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



    def add_subject_id(self, subject_id):
        self.add_constant_column("B", subject_id)

    def add_allowed(self, allowed_value):
        self.add_constant_column("D", allowed_value)

    def add_clock_information(self, clock_info):
        self.add_constant_column("E", clock_info)

    def add_datafile_basename(self, basename):
        self.add_constant_column("F", basename)

    def add_display_refresh_rate(self, refresh_rate_hz):
        self.add_constant_column("G", refresh_rate_hz)

    def add_experiment_version(self, experiment_version):
        self.add_constant_column("H", experiment_version)

    def add_group(self, group_num):
        self.add_constant_column("I", group_num)

    def add_handedness(self, hand):
        self.add_constant_column("J", hand)

    def add_narguid(self, narguid):
        self.add_constant_column("L", narguid)

    def add_runtime_capabilities(self, capabilities):
        self.add_constant_column("P", capabilities)

    def add_runtime_version(self, runtime_version):
        self.add_constant_column("Q", runtime_version)

    def add_runtime_version_expected(self, runtime_version):
        self.add_constant_column("R", runtime_version)

