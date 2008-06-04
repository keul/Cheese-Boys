# -*- coding: utf-8 -

import random

class RandomGenerator(object):
    """This random class may be only a wrapper for standard pygame random module...
    Buy may be that this is overwritten during unit-testing
    """  

    def choice(self, sequence):
        return random.choice(choice)

    def randint(self, int1, int2):
        return random.randint(int1, int2)

cbrandom = RandomGenerator()