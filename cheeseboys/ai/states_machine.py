# -*- coding: utf-8 -

# All code from this module is taken from the very good
# "Beginning Game Development with Python and Pygame - 
# From Novice to Professional", by Will McGugan.
# See http://www.willmcgugan.com/

class State(object):
    
    def __init__(self, name):        
        self.name = name
        
    def do_actions(self):
        raise NotImplementedError
        
    def check_conditions(self):        
        raise NotImplementedError    
    
    def entry_actions(self):        
        raise NotImplementedError    
    
    def exit_actions(self):        
        raise NotImplementedError
        
        
class StateMachine(object):
    
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
        
      
    
class GameEntity(object):
    
    def __init__(self, world, name, image):
        self.world = world
        self.name = name
        self.image = image
        self.location = Vector2(0, 0)
        self.destination = Vector2(0, 0)
        self.speed = 0.
        
        self.brain = StateMachine()
        
        self.id = 0
        
    def render(self, surface):
        
        x, y = self.location
        w, h = self.image.get_size()
        surface.blit(self.image, (x-w/2, y-h/2))   
        
    def process(self, time_passed):
        
        self.brain.think()
        
        if self.speed > 0. and self.location != self.destination:
            
            vec_to_destination = self.destination - self.location        
            distance_to_destination = vec_to_destination.get_length()
            heading = vec_to_destination.get_normalized()
            travel_distance = min(distance_to_destination, time_passed * self.speed)
            self.location += travel_distance * heading
        
