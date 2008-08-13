# -*- coding: utf-8 -

import pygame
from cheeseboys import utils

class GameSprite(pygame.sprite.Sprite):
    """Base character for game sprite. This is a normal pygame sprite with some other methods.
    A GameSprite is always used inside a Level object.
    """
    
    def __init__(self, *containers):
        pygame.sprite.Sprite.__init__(self, *containers)
        self.currentLevel = None
        self._x = self._y = None
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

    @property
    def position(self):
        """Character position as tuple"""
        return (self.x + self.rect.width/2, self.y+self.rect.height)
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
        return ""

    def addToGameLevel(self, level, firstPosition):
        self.currentLevel = level
        self.x, self.y = firstPosition
        rectPosition = level.transformToScreenCoordinate(firstPosition)
        try:
            self.rect = self.image.get_rect(topleft=rectPosition)
        except AttributeError:
            pass

    def checkCollision(self, x, y):
        """Check collision of this sprite with other.
        Params x and y are used to adjust the collire_rect before detection.
        BBB: move this logic in the Level?
        BBB: use of the zindex info?
        """
        x, y = utils.normalizeXY(x, y)
        
        collide_rect = self.collide_rect
        collide_rect.move_ip(x,y)
        collideGroups = (self.currentLevel['physical'],)
        for group in collideGroups:
            rects = [x.collide_rect for x in group.sprites() if x is not self]
            for rect in rects:
                if collide_rect.colliderect(rect):
                    return True
        return False

    @property
    def collide_rect(self):
        """For base sprite, the collide rect is the same as the rect attribute. You probably wanna overwrite this
        """
        return self.rect

    def move(self, x, y):
        """Move the sprite, relative to current point"""
        self.x+=x
        self.y+=y
        #self.rect.move_ip(x, y)
        self.refresh()
