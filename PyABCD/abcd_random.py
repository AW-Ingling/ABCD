import sys
import random



class ABCDRandom():

    RANDOM_SEED_MIN = -2147483648
    RANDOM_SEED_MAX = 2147483647

    def __init__(self):
        self.seed = None
        self.make_seed()

    def make_seed(self):
        self.seed = random.randint(self.RANDOM_SEED_MIN, self.RANDOM_SEED_MAX)
        random.seed(self.seed)

    def random(self):
        return random.random()

