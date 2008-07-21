# -*- coding: utf-8 -

from cheeseboys.ai import State, StateMachine
from cheeseboys import cblocals
from cheeseboys.cbrandom import cbrandom

class BaseStateExploring(State):   

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


class BaseStateWaiting(State):   

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



class BaseStateHunting(State):   

    def __init__(self, character):
        State.__init__(self, "hunting", character)

    def do_actions(self, time_passed):
        character = self.character
        character.moveBasedOnNavPoint(time_passed, character.enemyTarget.position)

    def check_conditions(self):
        character = self.character
        enemy = character.enemyTarget
        if not enemy.isAlive:
            return "waiting"
        
        if character.distanceFrom(enemy)>character.sightRange*2:
            return "waiting"
        
        if cbrandom.rool100() < self._getChanceForAttackBasedOnDistance(character.distanceFrom(enemy), character.attackRange):
            return "attacking"
        
        return None

    def entry_actions(self, old_state_name):
        self.character.speed = self.character.maxSpeed

    def exit_actions(self, new_state_name):
        if new_state_name!="attacking":
            self.character.enemyTarget = None


class BaseStateAttacking(State):   

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
        enemy = character.enemyTarget

        if character.isAttacking():
            return None

        if enemy and not enemy.isAlive:
            return "waiting"

        # BBB...
        if cbrandom.randint(1,100)<=25:
            return "retreat"

        if character.distanceFrom(enemy)>character.attackRange:
            return "hunting"
        
        return None

    def entry_actions(self, old_state_name):
        self.character.speed = self.character.maxSpeed

    def exit_actions(self, new_state_name):
        character = self.character
        character.stopAttack()
#        if new_state_name!="hunting":
#            self.character.enemyTarget = None


class BaseStateHit(State):
    """This state is the base state for a character hit by a blow.
    Commonly only external action can move a character in this state.
    """

    def __init__(self, character):
        State.__init__(self, "hitten", character)
        self.collected_distance = 0
        self.distance_to_move = None
        self.old_state_name = None

    def do_actions(self, time_passed):
        character = self.character
        character.moveBasedOnHitTaken(time_passed)
        self.collected_distance += time_passed * character.speed

    def check_conditions(self):
        """Always return to last action before the Hit.
        If the last was an attack then we return to the hunting state (or an "aatack in the air" is performed).
        """
        if self.collected_distance>=self.distance_to_move:
            if self.old_state_name == "attacking":
                return "hunting"
            return self.old_state_name
        return None

    def entry_actions(self, old_state_name):
        self.character.speed = cbrandom.randint(cblocals.HIT_MOVEMENT_SPEED/2, cblocals.HIT_MOVEMENT_SPEED)
        self.distance_to_move = 50
        self.old_state_name = old_state_name

    def exit_actions(self, new_state_name):
        self.collected_distance = 0
        self.distance_to_move = None


class BaseStateRetreat(State):
    """The character will perform a withdraw.
    """

    def __init__(self, character):
        State.__init__(self, "retreat", character)
        self.collected_distance = 0
        self.distance_to_move = None

    def do_actions(self, time_passed):
        character = self.character
        character.moveBasedOnRetreatAction(time_passed)
        self.collected_distance += time_passed * character.speed

    def check_conditions(self):
        """The character exit this state only when hit effect ends"""
        if self.collected_distance>=self.distance_to_move:
            return "resting"
        return None

    def entry_actions(self, old_state_name):
        character = self.character
        character.speed = character.maxSpeed * 2
        character.navPoint = None
        character.moving(False)
        self.distance_to_move = 50

    def exit_actions(self, new_state_name):
        self.collected_distance = 0
        self.character.speed = self.character.maxSpeed
        self.distance_to_move = None


class BaseStateResting(State):
    """The character will rest for a while.
    """

    def __init__(self, character):
        State.__init__(self, "resting", character)
        self.rest_time = .5
        self.collected_rest_time = 0

    def do_actions(self, time_passed):
        self.collected_rest_time += time_passed

    def check_conditions(self):
        """The character exit this state only when hit effect ends"""
        if self.collected_rest_time>=self.rest_time:
            return "waiting"
        return None

    def exit_actions(self, new_state_name):
        self.collected_rest_time = 0

    def isLockedState(self):
        return True





# ******* ladies and gentlemen: The Amazing State Machine *******

class BaseStateMachine(StateMachine):
    """State machine for very base character"""

    def __init__(self, character):
        self._character = character
        states = (BaseStateWaiting(character),
                  BaseStateExploring(character),
                  BaseStateHunting(character),
                  BaseStateAttacking(character),
                  BaseStateHit(character),
                  BaseStateRetreat(character),
                  BaseStateResting(character),
                  )
        StateMachine.__init__(self, states)