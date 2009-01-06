# -*- coding: utf-8 -

from cheeseboys.cbrandom import cbrandom
from cheeseboys import cblocals

TH0_MISS = "miss"
TH0_HIT = "hit"
TH0_SURPRISE_HIT = "surprise hit"
TH0_MISS_CRITICAL = "miss (critical)"
TH0_HIT_CRITICAL = "critical hit"
TH0_HIT_SURPRISE_CRITICAL = "critical surprise hit"

TH0_ALL_SUCCESSFUL = (TH0_HIT, TH0_SURPRISE_HIT, TH0_HIT_CRITICAL, TH0_HIT_SURPRISE_CRITICAL)
TH0_BACKSTABBING = (TH0_SURPRISE_HIT, TH0_SURPRISE_HIT)

class TH0(object):
    """Object of this class is used for combat mechanism.
    This class repr the power of a character to hit in combat someone (or something).
    
    The thrown for an hit procedure is based on the roll of 1d20.
    If the roll, plus the character level_bonus to hit, plus others bonus or malus reach the
    target AC value, the target is hit.
    """
    
    def __init__(self, character, level_bonus):
        self.character = character
        self._level_bonus = level_bonus
    
    def roll(self):
        """Service method to roll 1d20"""
        return cbrandom.throwDices("1d20")

    def attack(self, target, bonusToAttackRoll=0):
        """Check if an attack roll hit or miss a target.
        Every character has a +4 to the roll if unseen by the target
        """
        targetAC = target.AC
        attackRoll = self.roll()
        if attackRoll==1:
            # a natural 1 always miss
            return TH0_MISS_CRITICAL

        if self.character.stealth and not target.canSeeHiddenCharacter(self.character):
            surpriseAttack = True
        else:
            surpriseAttack = False

        if attackRoll==20:
            # a natural 20 always hit
            if surpriseAttack:
                return TH0_HIT_SURPRISE_CRITICAL
            return TH0_HIT_CRITICAL

        if surpriseAttack:
            bonusToAttackRoll+=4

        attackRoll = attackRoll + bonusToAttackRoll

        if attackRoll>=targetAC:
            if surpriseAttack:
                return TH0_SURPRISE_HIT
            return TH0_HIT
        
        return TH0_MISS

