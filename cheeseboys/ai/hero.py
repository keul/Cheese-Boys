# -*- coding: utf-8 -

from cheeseboys.ai import State, StateMachine
from base_brain import BaseStateHunting, BaseStateAttacking
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
            return "waiting"
        
        if character.distanceFrom(enemy)<=character.attackRange and cbrandom.randint(1,50)==1:
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
        return "controlled"



class HeroStateMachine(StateMachine):
    """State machine for the hero.
    The state machine is used rarely... you are controlling the game!
    """

    def __init__(self, character):
        self._character = character
        states = (HeroStateControlled(character),
                  HeroStateHunting(character),
                  HeroStateAttacking(character),
                  )
        StateMachine.__init__(self, states)


