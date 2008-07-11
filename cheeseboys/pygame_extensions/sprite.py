# -*- coding: utf-8 -

import pygame

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
        """Return top left position for this sprite"""
        topleft = self.rect.topleft
        if x or y:
            return (topleft[0]+x, topleft[1]+y)
        return topleft

#    def _getX(self):
#        tx = self.currentLevel.topleft[0]
#        #return tx + self.rect.centerx
#        return self._x# - self.rect.width/2
    def _setX(self, newx):
        self._x = newx
    #x = property(_getX, _setX, doc="""The sprite X position""")
    #x = property(lambda self: self.rect.centerx, _setX, doc="""The sprite X position""")
    #x = property(lambda self: self._x, _setX, doc="""The sprite X position""")
    x = property(lambda self: self._x, _setX, doc="""The sprite X position""")

#    def _getY(self):
#        ty = self.currentLevel.topleft[1]
#        topleft = self.topleft()
#        #return ty + self.rect.bottom-3
#        return self._y# + self.rect.height - 3
    def _setY(self, newy):
        self._y = newy
    #y = property(_getY, _setY, doc="""The sprite Y position""")
    #y = property(lambda self: self.rect.bottom-3, _setY, doc="""The sprite Y position""")
    #y = property(lambda self: self._y, _setY, doc="""The sprite Y position""")
    y = property(lambda self: self._y, _setY, doc="""The sprite Y position""")

    @property
    def position(self):
        """Character position as tuple"""
        return (self.x + self.rect.width/2, self.y+self.rect.height-3)
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
        self.rect.midbottom = (x, y-3)

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
        self.rect = self.image.get_rect(topleft=rectPosition)

    def move(self, x, y):
        """Move the sprite, relative to current point"""
        self.x+=x
        self.y+=y
        #self.rect.move_ip(x, y)
        self.refresh()
