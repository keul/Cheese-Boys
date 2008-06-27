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
    
    def generateRandomPoint(self, fromPoint=(), maxdistance=0):
        """Generate a random point on the level.
        You can use this giving a distance and s start point to get a random point near that position.
        Normally the point is taken at random on level dimension.
        """
        if fromPoint and maxdistance:
            offset_x = cbrandom.randint(-maxdistance,maxdistance)
            offset_y = cbrandom.randint(-maxdistance,maxdistance)
            startX = fromPoint[0] - maxdistance
            endX = fromPoint[0] + maxdistance
            startY = fromPoint[1] - maxdistance
            endY = fromPoint[1] + maxdistance
        else:
            # If one of the not required param is missing, always use the normal feature
            startX = 1
            endX = self.levelSize[0]-1
            startY = 1
            endY = self.levelSize[1]-1
        return self.normalizePointOnLevel(cbrandom.randint(startX,endX), cbrandom.randint(startY,endY))

    def normalizePointOnLevel(self, x, y):
        """Given and xy pair, normalize this to make this point valid on screen coordinate"""
        if x<1: x=1
        elif x>self.levelSize[0]-1: x=self.levelSize[0]-1
        if y<1: y=1
        elif y>self.levelSize[1]-1: y=self.levelSize[1]-1 
        return x,y       

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