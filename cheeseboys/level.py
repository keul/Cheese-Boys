# -*- coding: utf-8 -*-

import pygame
from cheeseboys import cblocals, utils
from cheeseboys.cbrandom import cbrandom
from cheeseboys.pygame_extensions import GameSprite

class GameLevel(object):
    """This repr a game level.
    Character move inside a level using some of his methods.
    """
    
    def __init__(self, name, size, background=None):
        """Init a level object with a name and a dimension.
        If a background file name is given, this image is loaded as background.
        If you don't give a background then the level name (converted in a lowecase, less separated png file name)
        is used instead.
        If you really don't have a level image, please use a background parameter to None
        """
        self.name = name
        self.levelSize = size
        self.group_charas = None
        if background is None:
            background = name.lower().replace(" ","-")+".png"
        if background:
            self._background = utils.load_image(background, directory="levels")
        # Special group infos
        self.group_dead = None
    
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
        
        group = self.group_charas
        enemies = []
        for charas in group.sprites():
            if character.side!=charas.side and character.distanceFrom(charas)<=sight:
                #distances.append(character.v-charas.v)
                enemies.append(charas)
        if enemies:
            return cbrandom.choice(enemies)
        return None

    def draw(self, screen):
        """Draw the level"""
        if self._background:
            screen.blit(self._background, (0,0) )

    def hasBackground(self):
        """Check is this level has a background image"""
        return self._background is not None

    def generateDeadSprite(self, corpse):
        """Using a character (commonly... very commonly... a DEAD ones!), generate a corpse"""
        group_dead = self.group_dead
        sprite = GameSprite(group_dead)
        sprite.image = utils.getRandomImageFacingUp(corpse.images)
        curRect = corpse.rect
        newRect = pygame.Rect( (curRect.centerx-curRect.height/2, curRect.bottom-curRect.width), (curRect.height,curRect.width) )
        sprite.rect = pygame.Rect(newRect)
        group_dead.add()
