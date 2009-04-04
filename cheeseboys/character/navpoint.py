# -*- coding: utf-8 -

from cheeseboys.utils import Vector2

class NavPoint(object):
    """A class for store the target of movement action of GameCharacter sprites,
    and manage the path to follow.
    """
    
    def __init__(self, character):
        self._character = character
        self._navPoint = None
        self.computed_path = []
    
    def set(self, value):
        if type(value)==tuple:
            value = Vector2(value)
        self._character.moving(True)
        self._character.compute_path(value)
        self.next()
    
    def get(self):
        return self._navPoint

    def reset(self):
        self._navPoint = None
        self._character.moving(False)

    def next(self):
        """Get the next navPoint from the computed_path list"""
        try:
            self._navPoint = Vector2(self.computed_path.pop(0))
        except IndexError:
            self._navPoint = None
            self._character.moving(False)

    def reroute(self):
        """Re-compute the route to the target"""
        try:
            self._character.compute_path(self.computed_path[-1])
        except IndexError:
            pass
        self.next()

    def as_tuple(self):
        return self._navPoint.as_tuple()
    
    def __nonzero__(self):
        if self._navPoint is None:
            return False
        return True
    
    def __str__(self):
        st = 'to %s' % self._navPoint
        if self.computed_path:
            st+= '(' + ', '.join(self.computed_path) + ')'
        return st

