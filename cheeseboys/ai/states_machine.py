# -*- coding: utf-8 -

# All code from this module is taken from the very good
# "Beginning Game Development with Python and Pygame - 
# From Novice to Professional", by Will McGugan.
# See http://www.willmcgugan.com/

class State(object):
    """Base class for the state machine's states.
    This will be subclassed for every new existing states
    """
    
    def __init__(self, name, character):        
        self.name = name
        self.character = character
        self.level = character.currentLevel
        
    def do_actions(self):
        raise NotImplementedError
        
    def check_conditions(self):        
        raise NotImplementedError    
    
    def entry_actions(self):        
        raise NotImplementedError    
    
    def exit_actions(self):        
        raise NotImplementedError
        
        
class StateMachine(object):
    """The state machine class"""
    
    def __init__(self):
        self.states = {}
        self.active_state = None
    
    
    def add_state(self, state):
        self.states[state.name] = state
        
        
    def think(self):
        if self.active_state is None:
            return
        
        self.active_state.do_actions()        

        new_state_name = self.active_state.check_conditions()
        if new_state_name is not None:
            self.set_state(new_state_name)
        
    
    def set_state(self, new_state_name):
        
        if self.active_state is not None:
            self.active_state.exit_actions()
        self.active_state = self.states[new_state_name]        
        self.active_state.entry_actions()
        
      
    
class IntelligenteEntity(object):
    """All Character class that also subclass this class can take action in automatic.
    So non-playing character MUST subclass this (or better, allNPC that need to move
    and interact with the World).
    """ 
    
    def __init__(self):      
        self.brain = StateMachine()  
        
    def process(self, time_passed):
        
        self.brain.think()
        
        if self.speed > 0. and self.location != self.destination:
            
            vec_to_destination = self.destination - self.location        
            distance_to_destination = vec_to_destination.get_length()
            heading = vec_to_destination.get_normalized()
            travel_distance = min(distance_to_destination, time_passed * self.speed)
            self.location += travel_distance * heading
        
