# -*- coding: utf-8 -

from cheeseboys import cblocals

class memoize_playingtime(object):
    """A playing-time based memoization; store the same value until the playing time is the same
    (and also the parameters).
    """
    def __init__ (self, f):
        self.f = f
        self.mem = {}

    def __call__ (self, *args, **kwargs):
        memoized = None
        if (args, str(kwargs)) in self.mem:
            memoized_time, memoized = self.mem[args, str(kwargs)]
            if memoized_time!=cblocals.playing_time:
                memoized = None
            #else:
            #    print "cache it"
        if not memoized:
            #print "cache miss"
            memoized = self.f(*args, **kwargs)
            self.mem[args, str(kwargs)] = (cblocals.playing_time, memoized)
        return memoized


class memoize_charasimage(object):
    """A special memoize decorator for speed up the render if the image property of Character sprites"""
    def __init__ (self, f):
        self.f = f
        self.mem = {}

    def __call__ (self, character):
        memoized = None
        if character in self.mem:
            image, _attackDirection, _isMoving, _mustChangeImage, _lastUsedDirection = self.mem[character]
            if character._attackDirection==_attackDirection and \
               character._isMoving==_isMoving and \
               character._mustChangeImage==_mustChangeImage and \
               character._lastUsedDirection==_lastUsedDirection:
                return image
        # There I need to return a new value
        image = self.f(character)
        self.mem[character] = (image, character._attackDirection,
                               character._isMoving, character._mustChangeImage, character._lastUsedDirection)
        return image

