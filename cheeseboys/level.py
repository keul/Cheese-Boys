# -*- coding: utf-8 -*-

from cheeseboys import cblocals
from cheeseboys.cbrandom import cbrandom
from cheeseboys.utils import Vector2

class GameLevel(object):
    """This repr a game level.
    Character move inside a level using some of his methods.
    """
    
    def __init__(self, name, size):
        self.name = name
        self.levelSize = size
        self.charasGroup = None
    
    def generateRandomPoint(self):
        return cbrandom.randint(1,cblocals.SCREEN_SIZE[0]-1), cbrandom.randint(1,cblocals.SCREEN_SIZE[1]-1)
    
    def addCharacter(self, character, firstPosition):
        """Add a character to this level at given position"""
        character.addToGameLevel(self, firstPosition)
    
    def getCloserEnemy(self, character, sight=None):
        """Return an enemy in the character sight"""
        if not sight:
            sight = character.sightRange
        
        group = self.charasGroup
        enemies = []
        for charas in group.sprites():
            if character.side!=charas.side and character.distanceFrom(charas)<=sight:
                #distances.append(character.v-charas.v)
                enemies.append(charas)
        if enemies:
            return cbrandom.choice(enemies)
        return None