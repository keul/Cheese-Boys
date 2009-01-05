# -*- coding: utf-8 -

import logging
import pygame
from pygame.locals import *
from cheeseboys import cblocals

class Stealth(object):
    """This class groups all feats of a Character to go in stealth-mode and hide in shadows.
    This class also contains all method needed to resists to a stealth movement.
    """
    
    def __init__(self):
        """The character stealth overall ability level"""
        self.stealthLevel = 0
        """The stealth status (if the character is trying to hide himself or not)"""
        self.stealth = False
        # Anti-stealth attributes
        self._stealthEnemies = {}
    
    @property
    def stealthIndex(self):
        """The overall current stealth index of this character.
        This is a real value from 0 (invisible) to 1 (fully visible).
        Values lower that 0.1 are uncommon for the game usage.

        The "stealthLevel" attribute of the current level will also modify the value. This real value is normally 1
        (no help and no malus for hiding in shadows).
        A darker level can have a value lower than 1 (0.9, 0.9, ...).
        A too clear place (as an indoor with many light) may raise up this value (1.1, ...).

        """
        if not cblocals.GAME_STEALTH:
            return 1.

        if not self.stealth or not self.stealthLevel:
            return 1.
        
        level_stealth = self.currentLevel.stealthLevel
        
        if self._isMoving:
            return .7 * level_stealth
        
        return .5 * level_stealth

    def checkForStealthTiming(self):
        """This method return the number of millisecond needed from the character to perform a new
        check to find an hidden enemy.
        This value is influenced from the character level of experience (in the major part) but a little
        also from the character stealthLevel.
        
        The base timing is:
        10 seconds for expereince level 1 or less
        8 seconds for expereince level 2 or less
        
        and the formula is:
        int(base_timing - base_timing * (stealthLevel * .05))
        
        so for every value of stealthLevel the timing is lowered of a 5%
        """
        experienceLevel = self.experienceLevel
        stealthLevel = self.stealthLevel
        if experienceLevel <= 1:
            base_timing = 10000
        elif experienceLevel <= 2:
            base_timing = 8000

        return int(base_timing - base_timing * (stealthLevel * .05))

    def check_antiStealth(self, enemy):
        """Perform a check for find an hidden enemy.
        
        Higher is the character level, more often he can perform a check. This mean that a failure
        is only momentary. Later the character can perform the check again.
        
        The chance of success in the check depends on the enemy stealth level. Lower is the enemy stealthIndex,
        more hard will be the check to see him when hidden.
        
        @return: True if the attemp to find the enemy had success.
        """
        if not cblocals.GAME_STEALTH:
            return True
        stealthEnemies = self._stealthEnemies
        enemy_uid = enemy.UID()
        if not enemy.stealth:
            # The enemy is not trying to hide himself
            try:
                del stealthEnemies[enemy_uid]
            except KeyError:
                pass
            return True
        
        if stealthEnemies.has_key(enemy_uid):
            result = stealthEnemies[enemy_uid]['result']
            self._updateEnemyStatus(enemy_uid)
            return result
        
        return True

    def _updateEnemyStatus(self, enemy_uid):
        """Given an enemy UID, update his status timing
        """
        game_time = cblocals.game_time
        stealthEnemies = self._stealthEnemies
        enemy_timing = stealthEnemies[enemy_uid]['timing']
        if game_time-enemy_timing>enemy.checkForStealthTiming():
            del stealthEnemies[enemy_uid]
