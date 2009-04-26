# -*- coding: utf-8 -

from cheeseboys import cblocals

class memoize_playingtime(object):
    """A playing-time based memoization"""
    def __init__(self, function):
        self.function = function
        self.memoized = None
        self.playing_time = 0

    def __call__(self, *args):
        print self._zzz
        if not self.memoized or self.playing_time!=cblocals.playing_time:
            self.memoized = self.function(*args)
            self.playing_time = cblocals.playing_time
        return self.memoized


#class Memoize:
#    def __init__ (self, f):
#        self.f = f
#        self.mem = {}
#    def __call__ (self, *args, **kwargs):
#        if (args, str(kwargs)) in self.mem:
#            return self.mem[args, str(kwargs)]
#        else:
#            tmp = self.f(*args, **kwargs)
#            self.mem[args, str(kwargs)] = tmp
#            return tmp
