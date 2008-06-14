# -*- coding: utf-8 -

from cheeseboys.ai import State
from cheeseboys import cblocals

class FerrareseStateExploring(State):
        
    def _random_destination(self):
        """Set a destination at random on map"""
        self.character.setNavPoint(self.level.generateRandomPoint())    
    
    def do_actions(self):
        
        if randint(1, 20) == 1:
            self.random_destination()
            
    def check_conditions(self):
                        
        leaf = self.ant.world.get_close_entity("leaf", self.ant.location)        
        if leaf is not None:
            self.ant.leaf_id = leaf.id
            return "seeking"        
                
        spider = self.ant.world.get_close_entity("spider", NEST_POSITION, NEST_SIZE)        
        if spider is not None:
            if self.ant.location.get_distance_to(spider.location) < 100.:
                self.ant.spider_id = spider.id
                return "hunting"
        
        return None
    
    def entry_actions(self):
        
        self.ant.speed = 120. + randint(-30, 30)
        self.random_destination()