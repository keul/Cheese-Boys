# -*- coding: utf-8 -*-

from cheeseboys import cblocals
from cheeseboys.cbrandom import cbrandom

class GameLevel(object):
    """This repr a game level.
    Character move inside a level using some of his methods.
    """
    
    def __init__(self, name, size):
        self.name = name
        self.levelSize = size
    
    def generateRandomPoint(self):
        return cbrandom.randint(1,cblocals.SCREEN_SIZE[0]-1), cbrandom.randint(1,cblocals.SCREEN_SIZE[1]-1)
    
    def addCharacter(self, character, firstPosition):
        """Add a character to this level at given position"""
        character.addToGameLevel(self, firstPosition)