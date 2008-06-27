# -*- coding: utf-8 -

from cheeseboys.ai import State, StateMachine
from cheeseboys import cblocals
from cheeseboys.cbrandom import cbrandom

class FerrareseStateExploring(State):   

    def __init__(self, character):
        State.__init__(self, "exploring", character)

    def do_actions(self, time_passed):        
        self.character.moveBasedOnNavPoint(time_passed)
            
    def check_conditions(self):
        character = self.character
        enemy = self.character.currentLevel.getCloserEnemy(character, character.sightRange)        
        if enemy is not None:
            character.enemyTarget = enemy
            return "hunting"
        
        if not character.navPoint:
            return "waiting"
        
        return None
    
    def entry_actions(self, old_state_name):
        # "Relaxed" enemy never run... ;-)
        self.character.speed = self.character.maxSpeed * cbrandom.uniform(0.3, 0.6)
        self._chooseRandomDestination()


class FerrareseStateWaiting(State):   

    def __init__(self, character):
        State.__init__(self, "waiting", character)
        self.waiting_time = cbrandom.randint(0, 4)

    def do_actions(self, time_passed): 
        self.waiting_time -= time_passed
            
    def check_conditions(self):
        character = self.character
        level = character.currentLevel
        enemy = level.getCloserEnemy(character, character.sightRange)        
        if enemy is not None:
            character.enemyTarget = enemy
            return "hunting"
        
        if self.waiting_time<0:
            return "exploring"
        
        return None

    def entry_actions(self, old_state_name):
        self.waiting_time = cbrandom.randint(0, 4)



class FerrareseStateHunting(State):   

    def __init__(self, character):
        State.__init__(self, "hunting", character)

    def do_actions(self, time_passed):
        character = self.character
        character.moveBasedOnNavPoint(time_passed, character.enemyTarget.position)
            
    def check_conditions(self):
        character = self.character
        level = character.currentLevel
        enemy = character.enemyTarget
        if not enemy.isAlive:
            return "waiting"
        
        if character.distanceFrom(enemy)>character.sightRange*2:
            return "exploring"
        
        if character.distanceFrom(enemy)<=character.attackRange and cbrandom.randint(1,50)==1:
            return "attacking"
        
        return None

    def entry_actions(self, old_state_name):
        self.character.speed = self.character.maxSpeed

    def exit_actions(self, new_state_name):
        if new_state_name!="attacking":
            self.character.enemyTarget = None


class FerrareseStateAttacking(State):   

    def __init__(self, character):
        State.__init__(self, "attacking", character)

    def do_actions(self, time_passed):
        character = self.character
        enemy = character.enemyTarget
        character.moveBasedOnNavPoint(time_passed, enemy.position)
        if not character.isAttacking():
            character.setAttackState(character.getHeadingTo(enemy))
        else:
            character.updateAttackState(time_passed)
        
    def check_conditions(self):
        character = self.character
        level = character.currentLevel
        enemy = character.enemyTarget

        if character.isAttacking():
            return None

        if enemy and not enemy.isAlive:
            return "waiting"
        
        if character.distanceFrom(enemy)>character.attackRange:
            return "hunting"
        
        return None

    def entry_actions(self, old_state_name):
        self.character.speed = self.character.maxSpeed

    def exit_actions(self, new_state_name):
        if new_state_name!="hunting":
            self.character.enemyTarget = None




class FerrareseStateMachine(StateMachine):
    """State machine for a ferrarese"""

    def __init__(self, character):
        self._character = character
        states = (FerrareseStateWaiting(character),
                  FerrareseStateExploring(character),
                  FerrareseStateHunting(character),
                  FerrareseStateAttacking(character),
                  )
        StateMachine.__init__(self, states)