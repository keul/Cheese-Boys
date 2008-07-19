# -*- coding: utf-8 -

from cheeseboys.cbrandom import cbrandom
from cheeseboys import cblocals

class TH0(object):
    """Object of this class is used for combat mechanism.
    This class repr the power of a character to hit in combat someone (or something).
    
    The thrown for an hit procedure is based on the roll of 1d20.
    If the roll, plus the character level_bonus to hit, plus others bonus or malus reach the
    target AC value, the target is hit.
    """
    
    def __init__(self, level_bonus):
        self._level_bonus = level_bonus
    
    def roll(self):
        """Service method to roll 1d20"""
        return cbrandom.throwDices("1d20")

    def attack(self, targetAC, bonusToAttackRoll=0):
        """Check if an attack roll hit or miss a target"""
        attackRoll = self.roll()
        if attackRoll==1:
            # a natural 1 always miss
            return cblocals.TH0_MISS_CRITICAL
        if attackRoll==20:
            # a natural 20 always hit
            return cblocals.TH0_HIT_CRITICAL
        
        attackRoll = attackRoll + bonusToAttackRoll
        
        if attackRoll>=targetAC:
            return cblocals.TH0_HIT
        
        return cblocals.TH0_MISS