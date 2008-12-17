# -*- coding: utf-8 -

import pygame
from pygame.locals import *

from cheeseboys.ai import State, StateMachine
from base_brain import BaseStateHunting, BaseStateAttacking, BaseStateHit, BaseStateRetreat
from cheeseboys import cblocals
from cheeseboys.cbrandom import cbrandom

class HeroStateControlled(State):
    """The hero is moved by the player (I mean a human with a brain).
    Think this state like a "brain sleep state". 
    """

    def __init__(self, character):
        State.__init__(self, "controlled", character)

    def do_actions(self, time_passed):
        pass

    def check_conditions(self):
        return None

class HeroStateHunting(BaseStateHunting):   
    """You right clicked over a far enemy. Move toward him"""

    def do_actions(self, time_passed):
        """Even while the hero is using the brain, the player can prevent him from moving
        using keys.
        """
        if not pygame.key.get_pressed()[K_LCTRL]:
            BaseStateHunting.do_actions(self, time_passed)

    def check_conditions(self):
        character = self.character
        level = character.currentLevel
        enemy = character.enemyTarget

        if not enemy.isAlive:
            return "controlled"
        
        if character.distanceFrom(enemy)<=character.attackRange:
            return "attacking"
        
        return None


class HeroStateAttacking(BaseStateAttacking):
    """Different from base class because the player must be able to regain control of the hero.
    """

    def do_actions(self, time_passed):
        """Changes from the base do_actions: we need to handle the CTRL key here"""
        character = self.character
        enemy = character.enemyTarget
        if not pygame.key.get_pressed()[K_LCTRL]:
            character.moveBasedOnNavPoint(time_passed, enemy.position)
        if not character.isAttacking():
            character.setAttackState(character.getHeadingTo(enemy))
        else:
            character.updateAttackState(time_passed)

    def check_conditions(self):
        """Continue attacking until other command or enemy dead"""
        character = self.character
        enemy = character.enemyTarget

        if character.isAttacking():
            return None

        if enemy and not enemy.isAlive:
            return "controlled"

        if character.distanceFrom(enemy)>character.attackRange:
            return "hunting"
        
        return None


class HeroStateHit(BaseStateHit):
    """Like BaseStateHit, but after the hit animation control return to last state"""

class HeroStateMachine(StateMachine):
    """State machine for the hero.
    The state machine is used rarely... you are controlling the game!
    """

    def __init__(self, character):
        self._character = character
        states = (HeroStateControlled(character),
                  HeroStateHunting(character),
                  HeroStateAttacking(character),
                  HeroStateHit(character),
                  BaseStateRetreat(character),
                  )
        StateMachine.__init__(self, states)


