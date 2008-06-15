# -*- coding: utf-8 -

import random

class RandomGenerator(object):
    """This random class may be only a wrapper for standard pygame random module...
    Buy may be that this is overwritten during unit-testing
    """  

    def choice(self, sequence):
        return random.choice(sequence)

    def randint(self, int1, int2):
        return random.randint(int1, int2)

    def uniform(self, a, b):
        return random.uniform(a, b)

cbrandom = RandomGenerator()