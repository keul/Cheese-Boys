# -*- coding: utf-8 -

import pygame
from pygame.locals import *

from cheeseboys.vector2 import Vector2
from cheeseboys.attack import Attack

class Warrior(object):
    """This class groups all feats of a Character that can fight in melee combat"""
    
    def __init__(self, attackTime, afterAttackRestTime):
        self._attackDirection = None
        self.attackHeading = self.lastAttackHeading = None
        self._attackRange = 24
        self._attackEffect = 10
        self._attack = None
        self._attackColor = (255, 255, 255, 200)
        self._attackLineWidth = 2
        self._attackTimeCollected = self._attackAnimationTimeCollected = 0
        self._attackTime = attackTime
        self._afterAttackRestTime = afterAttackRestTime
        self._attackAnimationTime = attackTime/2
        self.attackDamage = "1d6"
    
    def setAttackState(self, heading):
        """Set the character attack versus an heading direction.
        For duration of the attack the character can still moving, but will face the direction attacked.
        """
        direction = self._generateDirectionFromHeading(heading)
        self.attackHeading = self.lastAttackHeading = heading
        self._attackDirection = direction
        self._mustChangeImage = True

    def updateAttackState(self, time_passed):
        """Called to add some time to the attack time.
        This method control how long the attack is in action.
        """
        if self._attackTimeCollected<self._attackTime + self._afterAttackRestTime:
            self._attackTimeCollected+=time_passed
        else:
            self.stopAttack()

    def drawAttack(self, surface, time_passed):
        """Draw an attack effect on a surface in the attack heading direction.
        This method do nothing if isAttacking method return False.
        First this method get a point (call this attackEffectCenterVector) using the heading of the attack
        far from the character by a value equals to _attackRange/2 property of this character.
        This attackEffectCenterVector is a point from which we draw an X, thar repr charas attack.
        """
        if not self.isAttacking():
            return

        attackOriginVector = Vector2(self.physical_rect.center)
        if not self._attack:
            self._attack = Attack(self, attackOriginVector, self._attackRange, self._attackEffect, self._attackColor, self._attackLineWidth)

        self._attackAnimationTimeCollected+=time_passed
        if self._attackAnimationTimeCollected<self._attackAnimationTime/2:
            self._attack.drawPhase1(surface, attackOriginVector)
        elif self._attackAnimationTimeCollected<self._attackAnimationTime:
            self._attack.drawPhase2(surface, attackOriginVector)
        # else: pass

    def isAttacking(self):
        """Test if this charas is making an attack"""
        if self.attackHeading:
            return True
        return False

    def stopAttack(self):
        """Stop attack immediatly, resetting all attack infos"""
        self._attackDirection = self.attackHeading = self._attack = None
        self._attackTimeCollected = self._attackAnimationTimeCollected = 0

    @property
    def attackRange(self):
        """The range of the character's attacks"""
        return self._attackRange