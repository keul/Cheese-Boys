# -*- coding: utf-8 -

from cheeseboys.ai import State, StateMachine
from base_brain import BaseStateHunting, BaseStateAttacking, BaseStateHit, BaseStateResting, BaseStateRetreat
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

    def do_actions(self, time_passed):
        character = self.character
        enemy = character.enemyTarget
        character.moveBasedOnNavPoint(time_passed, enemy.position)
        if not character.isAttacking():
            character.setAttackState(character.getHeadingTo(enemy))
        else:
            character.updateAttackState(time_passed)
        
    def check_conditions(self):
        """Alway exit after the first attack"""
        if not self.character.isAttacking():      
            return "controlled"
        return None


class HeroStateHit(BaseStateHit):
    """Like BaseStateHit, but after the hit animation control return to last state"""

    def __init__(self, character):
        BaseStateHit.__init__(self, character)
        self.lastState = None

    def check_conditions(self):
        """The character exit this state only when hit effect ends"""
        if self.collected_distance>=self.distance_to_move:
            return "controlled"
        return None

    def exit_actions(self, new_state_name):
        BaseStateHit.exit_actions(self, new_state_name)
        self.character.speed = self.character.maxSpeed


class HeroStateResting(BaseStateResting):
    """The character will rest for a while (hero version)
    """

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
                  HeroStateResting(character),
                  )
        StateMachine.__init__(self, states)


