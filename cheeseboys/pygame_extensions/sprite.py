# -*- coding: utf-8 -

import logging

import pygame
from pygame.locals import *
from cheeseboys import cblocals, utils

class GameSprite(pygame.sprite.Sprite):
    """Base character for game sprite. This is a normal pygame sprite with some other methods.
    A GameSprite is always used inside a Level object.
    """
    
    def __init__(self, *containers):
        pygame.sprite.Sprite.__init__(self, *containers)
        self.currentLevel = None
        self._x = self._y = None
        self.name = None
        self.rect = None

    def update(self, time_passed):
        """Update method of pygame Sprite class.
        Keep updated sprite position on level.
        """
        pygame.sprite.Sprite.update(self, time_passed)
        self.refresh()

    def topleft(self, x=0, y=0):
        """Return top left rect info for this sprite.
        x and y can be final coordinate modifier.
        """
        topleft = self.rect.topleft
        if x or y:
            return (topleft[0]+x, topleft[1]+y)
        return topleft

    def _setX(self, newx):
        self._x = newx
    x = property(lambda self: self._x, _setX, doc="""The sprite X position""")

    def _setY(self, newy):
        self._y = newy
    y = property(lambda self: self._y, _setY, doc="""The sprite Y position""")

    def _setPosition(self, new_position):
        x, y = new_position
        self.x = x
        self.y = y        
    def _getPosition(self):
        if not self.x and not self.y:
            return ()
        return (self.x, self.y)
    position = property(_getPosition, _setPosition, doc="""Character position (midbottom) as tuple""")
    
    @property
    def position_int(self):
        """Same as position but in integer format"""
        x,y = self.position
        return (int(x), int(y))
    @property
    def v(self):
        """Return position as Vector2 object"""
        x,y = self.position
        return Vector2(x, y)

    def isNearTo(self, point):
        """Check if the sprite collision rect (the basement) is near to a point."""
        x, y = self.currentLevel.transformToScreenCoordinate(point)
        return self.collide_rect.collidepoint(x, y-3)

    def refresh(self):
        """Refresh sprite position based on x,y tuple"""
        x, y = self.toScreenCoordinate()
        self.rect.midbottom = (x, y)

    def toScreenCoordinate(self):
        """Return X,Y tuple information converting it back to screen position"""
        return self.currentLevel.transformToScreenCoordinate(self.position_int)

    def getTip(self):
        """Print a tip text near the character.
        Override this for subclass if you want this"""
        return None

    def addToGameLevel(self, level, firstPosition):
        """Add this sprite to a level.
        You must set an initial position that become the midbottom position of the sprite rect.
        """
        self.currentLevel = level
        self.x, self.y = firstPosition
        rectPosition = level.transformToScreenCoordinate(firstPosition)
        self.rect.midbottom = rectPosition

    def checkCollision(self, x, y):
        """Check collision of this sprite with other.
        Params x and y are used to adjust the collire_rect before detection.
        If a collision occurs, a SPRITE_COLLISION_EVENT is raised.
        BBB: use of the zindex info here can be useful?
        """
        x, y = utils.normalizeXY(x, y)
        
        collide_rect = self.collide_rect
        collide_rect.move_ip(x,y)
        collideGroups = (self.currentLevel['physical'],)
        for group in collideGroups:
            for sprite in group.sprites():
                if sprite is self:
                    continue
                sprite_rect = sprite.collide_rect
                if collide_rect.colliderect(sprite_rect):
                    event = pygame.event.Event(cblocals.SPRITE_COLLISION_EVENT, {'source':self, 'to': sprite})
                    pygame.event.post(event)
                    return True
        return False

    @property
    def collide_rect(self):
        """Return a rect used for collision in movement. This must be equals to sprite "foot" area.
        For general GameSprite, the collide rect is the same as the rect attribute.
        You probably wanna (must) overwrite this in all subclass!
        """
        return self.rect

    @property
    def physical_rect(self):
        """Return a rect used for collision (not collision with movement!)
        This must be equals to image's character total area.
        You probably wanna (must) overwrite this in all subclass!
        """
        return self.collide_rect

    def move(self, x, y):
        """Move the sprite, relative to current point"""
        self.x+=x
        self.y+=y
        #self.rect.move_ip(x, y)
        self.refresh()

    @classmethod
    def _loadEmptySprite(self, dimension, alpha=None, fillWith=None, colorKey=None):
        """Return Surface. Default setting is for blanck and not filled ones.
        You can enter alpha value, fill color and colorkey color for per-pixel-alpha.
        """
        surface = pygame.Surface(dimension, flags=SRCALPHA, depth=32)
        if fillWith:
            surface.fill(fillWith)
        if alpha is not None:
            surface.set_alpha(alpha)
        if colorKey:
            surface.set_colorkey(colorKey)
        return surface

    def addToGroups(self, *groups):
        """Add a sprite to multiple groups"""
        for g in groups:
            g.add(self)

    def triggetCollision(self, source):
        """This method can be overrided in subclasses. Is called every time a sprite
        collide with this sprite.
        Source is the sprite that collide. Base implementation does nothing at all.
        """
        pass

    @classmethod
    def manageCollisions(cls, source, to):
        """Class method for handling collision by sprites.
        If the source "sprite" collide with the "to" sprite, the triggetCollision method is called
        onto the "to" sprite.
        """
        to.triggetCollision(source)
        logging.debug("%s sprite collided with %s" % (source, to))