# -*- coding: utf-8 -*-

# The code in this class is originally taken from my (abandoned) Gareth's Quest project

import random


class UniqueObject(object):
    """Class for all game objects that must be unique in the game (in facts whathever has an UID)"""

    def __init__(self):
        self._uid = self._randomUID()

    @classmethod
    def _randomUID(cls, num_bits=64):
        """Return a string representing a bitfield num_bits long.
        Maximum artbitrarily set to 1024"""

        if num_bits < 1:
            raise RuntimeError("randomID called with negative (or zero) number of bits")
        if num_bits > 1024:
            raise RuntimeError("randomID called with too many bits (> 1024)")

        # create a num_bits string
        rnd = random.Random()
        tmp_id = 0
        for i in range(0, num_bits):
            tmp_id += int(rnd.randint(0, 1)) << i

        # The 2: removes the '0x' and :-1 removes the L
        rnd_id = hex(tmp_id)[2:-1]
        return rnd_id

    def UID(self):
        """Obtain the UID from this unique object"""
        return self._uid


class UniqueObjectRegistry(object):
    """A (commonly unique) instance of this will register all UID of unique objects in the game"""

    def __init__(self):
        self._registry = {}

    def register(self, unique):
        """Register a new object in this registry.
        @unique: An object with the UID method
        """
        try:
            uid = unique.UID()
        except AttributeError:
            raise TypeError("The object %s has no UID method" % unique)
        self._registry[uid] = unique

    def unregister(self, unique):
        """Unregister the stored unique object
        @unique: Can be an object with the UID method or the UID string
        """
        if type(unique) == str:
            uid = unique
        else:
            try:
                uid = unique.UID()
            except AttributeError:
                raise TypeError("The object %s has no UID method" % unique)
        del self._registry[uid]

    def __repr__(self):
        return self._registry.__repr__()
