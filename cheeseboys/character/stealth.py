# -*- coding: utf-8 -

import logging
import pygame
from pygame.locals import *
from cheeseboys import cblocals, cbrandom

class Stealth(object):
    """This class groups all feats of a Character to go in stealth-mode and hide in shadows.
    This class also contains all method needed to resists to a stealth attempt.
    
    Often the character that try to hide is called 'rogue'.
    
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
        
        if self.isMoving:
            base_index = .7
        else:
            base_index = .5

        index = base_index * level_stealth - ((self.stealthLevel-1+5)*.05)
        if index<.2:
            index=.2
        return index

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
        10 seconds for experience level 1 or less
        8 seconds for experience level 2 or less
        
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

    def getPreySightRangeReductionFactor(self):
        """This method return a the factor of reduction used for lower the prey sight range.
        The rogue always reduce the prey sight of a 10%, + 5% for every stealthLevel
        @return: a real value of 1 (100% of the sight), or lower (0.9 for 90%, ...)
        """
        reduction = 1.
        if self.stealth:
            reduction-= .1 + (.05*self.stealthLevel)
        return reduction

    @classmethod
    def generateStealthIndexFromHeadings(cls, rogueStealthIndex, prey, rogue):
        """Modify a stealthIndex of a rogue character checking also the headings of the characters
        
        The headings are commonly a couple of real values from -1 to +1 (a normalized x,y Vector2).
        The idea is that the rogue has good bonus if he's arriving from behind the prey.
        He gets no bonus if is arriving from beside the prey.
        Finally he get some malus if is arriving in front of the prey.
        
        This is not enough. If the rogue is not moving, he can get only malus, so he's counted like if
        he's always facing the prey.
        
        Again: is impossible to backstab the prey facing it directly!
        
        """
        rogueHeading = rogue.heading
        preyHeading = prey.heading
        print rogueHeading, preyHeading, rogueHeading + preyHeading
        
        # BBB: to be completed
        
        return rogueStealthIndex

    # *** below there are method used for notice hidden enemyes

    def check_antiStealth(self, enemy):
        """Perform a check for find an hidden enemy.
        
        Higher is the character level, more often he can perform a check. This mean that a failure
        is only momentary. Later the character can perform the check again.
        
        The chance of success in the check depends on the enemy stealth level. Lower is the enemy stealthIndex,
        more hard will be the check to see him when hidden.
        
        This value is also influenced by the character and enemy direction. If the rogue in moving in the same
        direction of the character (he is going away, or he is going behind the character), the rogue has
        some bonus!
        
        This method is really called once for a period of time (stealthRestTimeNeeded). Before this the value returned
        is cached. The cache is invalidated when:
        1) The rogue stop hiding.
        2) The rogue begin was still but now is moving.
        
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
            # Use cache only if the rogue is not moving, or he's moving like he was doing before
            if not self.isMoving or (self.isMoving and stealthEnemies[enemy_uid]['moving_status']):
                # BBB: fix here!
                print self.isMoving, stealthEnemies[enemy_uid]['moving_status']
                stealthEnemies[enemy_uid]['moving_status'] = self.isMoving
                result = stealthEnemies[enemy_uid]['result']
                self._updateEnemyStatus(enemy)
                return result
            else:
                logging.info("%s begin moving again" % self)
        
        enemyStealthIndex = enemy.stealthIndex
        
        # Now I need to modify the enemyStealthIndex based on the characters headings
        enemyStealthIndex = self.generateStealthIndexFromHeadings(enemyStealthIndex, self, enemy)
        
        # I need to check again for the hidden enemy
        rolled = cbrandom.cbrandom.uniform(0,1)
        result = rolled<enemyStealthIndex
        logging.info("%s try to find %s that have a stealth index of %0.2f: rolled %0.2f (%s)" % (self,
                                                                                   enemy,
                                                                                   enemyStealthIndex,
                                                                                   rolled,
                                                                                   result,
                                                                                   ))
        # now the moving status
        moving_status = self.isMoving

        stealthEnemies[enemy_uid] = {'result': result, 'timing': cblocals.game_time, 'moving_status': moving_status}
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
        """Check if this character could see an hidden target.
        @return: True if the target is not in stealth, or however if can see it
        """
        target_uid = target.UID()
        if not target.stealth:
            return True
        if self._stealthEnemies.has_key(target_uid):
            return self._stealthEnemies[target_uid]['result']
        return True

    def noticeForHiddenCharacter(self, enemy):
        """The use of this method force the character to see an hidden enemy"""
        enemy_uid = enemy.UID()
        try:
            del self._stealthEnemies[enemy_uid]
        except KeyError:
            pass
        logging.info("%s notice the %s presence" % (self, enemy))

