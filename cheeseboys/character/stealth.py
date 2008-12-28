# -*- coding: utf-8 -

import pygame
from pygame.locals import *

class Stealth(object):
    """This class groups all feats of a Character to go in stealth-mode and hide in shadows.
    This class also contains all method needed to resists to a stealth movement.
    """
    
    def __init__(self):
        self._stealthLevel = 0
        self.stealth = False
        # Anti-stealth attributes
        self._stealthEnemies = {}
    
    @property
    def stealthIndex(self):
        """The overall current stealth index of this character.
        This is a real value from 0 (invisible) to 1 (fully visible).
        Values lower that 0.1 are uncommon for the game usage.
        """
        if not self.stealth or not self._stealthLevel:
            return 1.
        
        if self._isMoving:
            return .7
        
        return .5

    def check_antiStealth(self, enemy):
        """Perform a check for find an hidden enemy.
        
        Higher is the character level, more often he can perform a check. This mean that a failure
        is only momentary. Later the character can perform the check again.
        
        The chance of success in the check depends on the enemy stealth level. Lower is the enemy stealthIndex,
        more hard will be the check to see him when hidden.
        
        @return: True if the attemp to find the enemy is succesfull
        """
        return True


