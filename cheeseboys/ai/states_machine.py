# -*- coding: utf-8 -

# All code from this module is taken (but modified) from the very good
# "Beginning Game Development with Python and Pygame - From Novice to Professional", by Will McGugan.
# See http://www.willmcgugan.com/

        
class StateMachine(object):
    """The state machine class.
    Istances of this class are the brain of the character that wanna move using AI intelligence.
    """
    
    def __init__(self, states=None):
        self.states = {}
        if not states:
            self.active_state = None
        else:
            for state in states:
                self._addState(state)
            self.active_state = states[0]


    def _addState(self, state):
        self.states[state.name] = state
        
    def think(self, time_passed):
        if self.active_state is None:
            return
        
        self.active_state.do_actions(time_passed)        

        new_state_name = self.active_state.check_conditions()
        if new_state_name is not None:
            self.setState(new_state_name)
        
    
    def setState(self, new_state_name):
        """Set a new state for the brain based on its name"""
        old_state = self.active_state
        if self.active_state is not None:
            self.active_state.exit_actions(new_state_name)
        self.active_state = self.states[new_state_name]    
        self.active_state.entry_actions(old_state.name)
        

class State(object):
    """Base class for the state machine's states.
    This will be subclassed for every new existing states
    """
    
    def __init__(self, name, character):        
        self.name = name
        self.character = character
        
    def do_actions(self, time_passed):
        """This unimplemented method is called first, for take some action based on this state"""
        raise NotImplementedError
        
    def check_conditions(self):
        """After every call of do_action, check_conditions is called to check if a state change must be done.
        State doesn't implements this method.
        """
        raise NotImplementedError    
    
    def entry_actions(self, old_state_name):
        """Optionally entry action called when this state became the current state.
        The old state name is passed.
        """
        pass
    
    def exit_actions(self, new_state_name):
        """Optionally entry action called when this state is left
        The new state name is passed.
        """
        pass

    def _chooseRandomDestination(self, maxdistance=200):
        """Set a destination at random on map"""
        self.character.setNavPoint(self.character.currentLevel.generateRandomPoint(fromPoint=self.character.position_int, maxdistance=maxdistance)) 
        
