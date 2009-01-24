# -*- coding: utf-8 -

import logging
import pygame
from pygame.locals import *
from cheeseboys import cblocals, cbrandom
from cheeseboys.utils import Vector2

class Stealth(object):
    """This class groups all feats of a Character to go in stealth-mode and hide in shadows.
    This class also contains all method needed to resists to a stealth attempt.
    
    Often the character that try to hide is called 'rogue'.
    The target, who can ignore the rogue presence, is called the prey.
    """
    
    def __init__(self):
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
        Values lower that 0.2 are not possibile.

        The "stealthLevel" attribute of the current level will also modify the value. This real value is normally 1
        (no help and no malus for hiding in shadows).
        A darker level can have a value lower than 1 (0.9, 0.9, ...).
        A too clear place (as an indoor with many light) may raise up this value (1.1, ...).

        Finally this index is obviously under the effect of the stealthLevel value of the rogue.

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

        # base_index * level_stealth - (5% for stealhLevel)
        index = base_index * level_stealth - ((self.stealthLevel-1 +8 )*.05) # BBB: debug value here
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
        also from the character stealthLevel (a good rogue is also a good prey).
        
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
    def adjustStealthIndexFromPosition(cls, rogueStealthIndex, rogue, prey):
        """Modify a passed stealthIndex of a rogue character checking also:
        1) the distance between rogue and prey
        2) the facing direction of the prey.
        
        The idea is that the rogue has good bonus if he's arriving from behind the prey.
        He gets no bonus if is arriving from beside the prey.
        Finally he get some malus if is arriving in front of the prey.
        
        Is also impossible that the prey didn't identify the hidden rogue if he's
        very near and directly in front of him!
        """
        distance = rogue.v.get_distance_to(prey.v)
        preySight = int(prey.sightRange * prey.getPreySightRangeReductionFactor())

        if distance<preySight/5:
            rogueStealthIndex*=1.3         # malus 30%
        elif distance<preySight/3:
            rogueStealthIndex*=1.2         # malus 20%
        elif distance<preySight/3*2:
            rogueStealthIndex*=1.1         # malus 10%
        
        # The rogue has malus if the prey is watching it: +25% (angle >=-30° and <=+30°)
        # The rogue has bonus if the prey is watching in the other direction: -20% (angle <=-150° and >=+150°)
        prey_to_rogue = Vector2.from_points(prey.position, rogue.position).normalize()
        angle_between = prey.heading.angle_between(prey_to_rogue)
        logging.debug("Prey heading: %s - Prey to rogue: %s - Angle: %s" % (prey.heading, prey_to_rogue, angle_between))
        
        if angle_between>=-30 or angle_between<=30:
            rogueStealthIndex*=1.3
        elif angle_between<=-150 or angle_between>=150:
            rogueStealthIndex*=.8
        
        if rogueStealthIndex>1.:
            rogueStealthIndex=1.
        elif rogueStealthIndex<.2:
            rogueStealthIndex=.2
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
        
        This method is really called once for a period of time (stealthRestTimeNeeded).
        
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
        
        enemyStealthIndex = enemy.stealthIndex        
        # Now I need to modify the enemyStealthIndex based on the characters headings
        enemyStealthIndex = self.adjustStealthIndexFromPosition(enemyStealthIndex, enemy, self)
        
        # I need to check again for the hidden enemy
        rolled = cbrandom.cbrandom.uniform(0,1)
        result = rolled<enemyStealthIndex
        logging.info("%s try to find %s that have a stealth index of %0.2f (base is %0.2f): rolled %0.2f (%s)" % (self,
                                                                                                                  enemy,
                                                                                                                  enemyStealthIndex,
                                                                                                                  enemy.stealthIndex,
                                                                                                                  rolled,
                                                                                                                  result,
                                                                                                                  ))
        stealthEnemies[enemy_uid] = {'result': result, 'timing': cblocals.game_time,}
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
        self._stealthEnemies[enemy_uid] = {'result': True, 'timing': cblocals.game_time,}
        logging.info("%s notice the %s presence" % (self, enemy))

