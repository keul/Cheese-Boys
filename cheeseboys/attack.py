# -*- coding: utf-8 -

import pygame
from pygame.locals import *

from cheeseboys import cblocals
from cheeseboys.vector2 import Vector2

class Attack(object):
    """Instances of this class wanna repr the attack action for every character.
    Commonly this is for basic charas weapon attacks.
    """
    
    def __init__(self, character, attackOriginVector, attackRange, attackEffect, attackColor, attackLineWidth):
        self._character = character
        self._attackColor = attackColor
        self._attackLineWidth = attackLineWidth
        self._attackRange = attackRange
        self._attackEffect = attackEffect
        self._updateRect(attackOriginVector)
        self._phase1 = self._phase2 = False
        self.rect = None

    def _updateRect(self, attackOriginVector):
        """Update stored rect position"""
        character = self._character
        attackRange = self._attackRange
        attackEffect = self._attackEffect
        attackEffectCenterVector = character.attackHeading*attackRange/2 + attackOriginVector
        attackEffectCenterVectorTuple = attackEffectCenterVector.as_tuple()
        self.rect = pygame.Rect( (attackEffectCenterVectorTuple[0]-attackEffect/2,attackEffectCenterVectorTuple[1]-attackEffect/2),
                                 (attackEffect,attackEffect) )
    
    def drawPhase1(self, surface, attackOriginVector):
        """Draw first phase of this attack"""
        if not self._phase1:
            self._phase1 = True
            event = pygame.event.Event(cblocals.ATTACK_OCCURRED_EVENT, {'character':self._character, 'attack':self})
            pygame.event.post(event)
        self._updateRect(attackOriginVector)
        pygame.draw.line(surface,
                         self._attackColor,
                         self.rect.topleft,
                         self.rect.bottomright,
                         self._attackLineWidth)

    def drawPhase2(self, surface, attackOriginVector):
        """Draw second phase of this attack"""
        if not self._phase2:
            self._phase2 = True
            event = pygame.event.Event(cblocals.ATTACK_OCCURRED_EVENT, {'character':self._character, 'attack':self})
            pygame.event.post(event)
        self.drawPhase1(surface, attackOriginVector)
        pygame.draw.line(surface,
                         self._attackColor,
                         self.rect.bottomleft,
                         self.rect.topright,
                         self._attackLineWidth)

