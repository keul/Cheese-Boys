# -*- coding: utf-8 -

def loadLevelByName(name, hero):
    """Load a level configuration using a string and return the configured level"""
    
    if name=="The South Bridge":
        from cheeseboys.level.levels_database import the_south_bridge
        return the_south_bridge.load(name, hero)
    if name=="Western Cavallotti Riverside 1":
        from cheeseboys.level.levels_database import western_cavallotti_riverside_1
        return western_cavallotti_riverside_1.load(name, hero)
    raise NameError("Level name %s not found" % name)