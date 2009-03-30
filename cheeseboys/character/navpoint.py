# -*- coding: utf-8 -

from cheeseboys.utils import Vector2

class NavPoint(object):
    """A class for store the target of movement action of GameCharacter sprites,
    and manage the path to follow.
    """
    
    def __init__(self):
        self._navPoint = None
        self._computed_path = []
    
    def set(self, value, computed_path):
        if type(value)==tuple:
            value = Vector2(value)
        self._navPoint = value
        self._computed_path = computed_path
    
    def get(self):
        return self._navPoint

    @property
    def computed_path(self):
        return self._computed_path

    def reset(self):
        self._navPoint = None

    def next(self):
        """Get the next navPoint from the computed_path list"""
        try:
            self._navPoint = Vector2(self._computed_path.pop(0))
        except IndexError:
            self._navPoint = None

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

