# -*- coding: utf-8 -

import logging
import pygame
from pygame.locals import *
from cheeseboys import cblocals, cbrandom

class Stealth(object):
    """This class groups all feats of a Character to go in stealth-mode and hide in shadows.
    This class also contains all method needed to resists to a stealth attempt.
    """
    
    def __init__(self):
        """The character stealth overall ability level"""
        self.stealthLevel = 0
        
        self._stealth = False
        self.stealthRestTimeNeeded = 5000
        self.last_stealth_timing = 0
        # Anti-stealth attributes
        self._stealthEnemies = {}

    def _setStealth(self, value):
        if value==False:
            logging.info("%s can't go in stealth mode again for %s millisec" % (self, self.stealthRestTimeNeeded))
            self.last_stealth_timing = cblocals.game_time
        self._stealth = value
    stealth = property(lambda self: self._stealth, _setStealth, doc="""The stealth status (if the character is trying to hide himself or not)""")

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

    def canStealthAgain(self):
        """After an hide in shadow attempt, the character can't hide again for a while.
        @return: True is the time until hide again (stealthRestTimeNeeded attribute) is passed.
        """
        return cblocals.game_time-self.last_stealth_timing>self.stealthRestTimeNeeded
        

    def getTimingBeforeCheckForStealth(self):
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
        
        # I have already tried a check for the enemy before
        if stealthEnemies.has_key(enemy_uid):
            result = stealthEnemies[enemy_uid]['result']
            self._updateEnemyStatus(enemy)
            return result
        
        # I need to check again for the hidden enemy
        rolled = cbrandom.cbrandom.uniform(0,1)
        result = rolled<enemy.stealthIndex
        logging.info("%s try to find %s that have a stealth index of %0.2f: rolled %0.2f (%s)" % (self,
                                                                                   enemy,
                                                                                   enemy.stealthIndex,
                                                                                   rolled,
                                                                                   result,
                                                                                   ))
        stealthEnemies[enemy_uid] = {'result': result, 'timing': cblocals.game_time}
        return result

    def _updateEnemyStatus(self, enemy):
        """Given an enemy, update his status timing.
        This method is crucial for repeat the check for an hidden enemy.
        """
        enemy_uid = enemy.UID()
        game_time = cblocals.game_time
        stealthEnemies = self._stealthEnemies
        enemy_timing = stealthEnemies[enemy_uid]['timing']
        if game_time-enemy_timing>enemy.getTimingBeforeCheckForStealth():
            del stealthEnemies[enemy_uid]

    def canSeeHiddenCharacter(self, target):
        """Check this character could see an hidden target
        @return: True if the target is not in stealth, or however if can see it
        """
        target_uid = target.UID()
        if not target.stealth:
            return True
        if self._stealthEnemies.has_key(target_uid):
            return self._stealthEnemies[target_uid]['result']
        return True