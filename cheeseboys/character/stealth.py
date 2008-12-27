# -*- coding: utf-8 -

import pygame
from pygame.locals import *

class Stealth(object):
    """This class groups all feats of a Character to go in stealth-mode and hide in shadows"""
    
    @property
    def stealthIndex(self):
        """The overall current stealth index of this character.
        This is a real value from 0 (invisible) to 1 (fully visible).
        Values lower that 0.1 or higher that 0.9 are uncommon for the game usage.
        """
        if not self.stealth or not self._stealthLevel:
            return 1
        
        if self._isMoving:
            return .7
        
        return .5