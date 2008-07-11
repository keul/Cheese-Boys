# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *
from cheeseboys import cblocals, utils
from cheeseboys.cbrandom import cbrandom
from cheeseboys.utils import Vector2
from cheeseboys.pygame_extensions import GameSprite

class GameLevel(object):
    """This repr a game level.
    Character move inside a level using some of its methods.
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
        self._topleft = (0,0)
        self._centeringSpeed = 50
        self._centeringHeading = None
        # Special group infos
        self.group_dead = None
    
    def _setTopLeft(self, topleft):
        self._topleft = topleft
    topleft = property(lambda self: self._topleft, _setTopLeft, doc="""The topleft drawing point inside the level bakcground image""")
    
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
        """Given and xy pair, normalize this to make this point valid on level coordinates"""
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
            self.topleft = self._normalizeDrawPart()
            screen.blit(self._background.subsurface(pygame.Rect(self.topleft, cblocals.GAME_SCREEN_SIZE) ), (0,0) )

    def _normalizeDrawPart(self, topleft=None, size=None):
        """Called to be sure that the draw portion of level isn't out of the level total surface"""
        x,y = topleft or self._topleft
        w,h = size or self.levelSize
        sw, sh = cblocals.GAME_SCREEN_SIZE
        if x<0:
            x=0
        if y<0:
            y=0
        if x+sw>w:
            x = w-sw
        if y+sh>h:
            y = h-sh
        return x,y
        
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

    @property
    def center(self):
        """The point at the center of the drawn level part"""
        topleft = self._topleft
        size = cblocals.GAME_SCREEN_SIZE
        return (topleft[0]+size[0]/2, topleft[1]+size[1]/2)

    def normalizeDrawPositionBasedOn(self, character, time_passed):
        """Slowly move drawn portion of the total level, for centering it on the given sprite"""
        if pygame.key.get_pressed()[K_LCTRL]:
            return
        referencePointOnScreen = character.position_int
        if self.isPointNearScreenCenter(referencePointOnScreen, (200,200) ):
            return
        heading = Vector2.from_points(self.center, referencePointOnScreen)
        heading.normalize()
        distance = time_passed * self._centeringSpeed
        movement = heading * distance
        x = movement.get_x()
        y = movement.get_y()
        self._topleft = (self._topleft[0]+x,self._topleft[1]+y)

    def isPointNearScreenCenter(self, refpoint, centerDimension):
        """This method return true if a given point is inside a rect of given dimension.
        The rect is placed at the screen center
        """
        cx, cy = self.center
        rect = pygame.Rect( (cx-centerDimension[0]/2,cy-centerDimension[1]/2), centerDimension )
        return rect.collidepoint(refpoint)

    def transformToLevelCoordinate(self, position):
        """Given a screen position, transform this to level absolute position"""
        x, y = position
        tx, ty = self.topleft
        return (tx+x, ty+y)