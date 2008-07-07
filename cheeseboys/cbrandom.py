# -*- coding: utf-8 -

import random
from numerichandlers import DiceHandler

class RandomGenerator(object):
    """This random class may be only a wrapper for standard pygame random module...
    Buy may be that this is overwritten during unit-testing
    """  

    def __init__(self, debug=False, values=[]):
        self._debug = debug
        self._preset_values = values
        if values:
            self._preset_values.reverse()

    def choice(self, sequence):
        return random.choice(sequence)

    def randint(self, int1, int2):
        return random.randint(int1, int2)

    def uniform(self, a, b):
        return random.uniform(a, b)

    def throwDices(self, dices, forceResultTo=0):
        """This very important function is used for the standard dices game mechanism.
        The forceResultTo, if used hack the throw of the dices.
        """
        if forceResultTo:
            return forceResultTo
    
        if self._debug:
            return self._getNextRandom()
    
        handler = DiceHandler(dices)
        numberOfDices, typeOfDice, bonus = handler.getValues()

        amount = 0
        for ndices in range(numberOfDices):
            # Every HD can be 1d8, 1d4...
            rndAmoun = random.randint(1, typeOfDice)+bonus
            if rndAmoun<1:
                rndAmoun = 1
            amount+= rndAmoun
        return amount

cbrandom = RandomGenerator()