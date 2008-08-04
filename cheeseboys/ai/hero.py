# -*- coding: utf-8 -

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

    def check_conditions(self):
        character = self.character
        level = character.currentLevel
        enemy = character.enemyTarget

        if not enemy.isAlive:
            return "controlled"
        
        if character.distanceFrom(enemy)<=character.attackRange:
            return "attacking"
        
        return None

    def exit_actions(self, new_state_name):
        if new_state_name!="attacking":
            self.character.enemyTarget = None


class HeroStateAttacking(BaseStateAttacking):
    """Different from base class is only needed for different check_conditions.
    """
        
    def check_conditions(self):
        """Alway exit after the first attack"""
        if not self.character.isAttacking():      
            return "controlled"
        return None


class HeroStateHit(BaseStateHit):
    """Like BaseStateHit, but after the hit animation control return to last state"""

    def __init__(self, character):
        BaseStateHit.__init__(self, character)
        self.rest_time = .3

    def check_conditions(self):
        """The character exit this state only when hit effect ends"""
        if self.collected_rest_time>=self.rest_time:
            return "controlled"
        return None



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


