# -*- coding: utf-8 -

import logging

import pygame
from pygame.locals import *
from cheeseboys import cblocals, utils
from cheeseboys.vector2 import Vector2
from cheeseboys.pygame_extensions.unique import UniqueObject

class GameSprite(pygame.sprite.Sprite, UniqueObject):
    """Base character for game sprite. This is a normal pygame sprite with some other methods.
    A GameSprite is always used inside a Level object.
    """
    
    _emptyTipStructure = {'text':"", 'color':(0,0,0)}
    
    def __init__(self, *containers):
        pygame.sprite.Sprite.__init__(self, *containers)
        UniqueObject.__init__(self)
        self.currentLevel = None
        self._x = self._y = None
        self.name = None
        self.rect = None

    def _setX(self, newx):
        self._x = newx
    x = property(lambda self: self._x, _setX, doc="""The sprite X position""")

    def _setY(self, newy):
        self._y = newy
    y = property(lambda self: self._y, _setY, doc="""The sprite Y position""")

    def _setPosition(self, new_position):
        x, y = new_position
        self._x = x
        self._y = y        
    def _getPosition(self):
        if not self.x and not self.y:
            return ()
        return (int(self.x), int(self.y))
    position = property(_getPosition, _setPosition, doc="""Character position (midbottom) as tuple""")

    @property
    def v(self):
        """Return position as Vector2 object"""
        return Vector2(self.position)


    def update(self, time_passed):
        """Update method of pygame Sprite class.
        Keep updated sprite position on level.
        """
        pygame.sprite.Sprite.update(self, time_passed)
        self.rect.midbottom = self.toScreenCoordinate()

    def topleft(self, x=0, y=0):
        """Return top left rect coordinate for this sprite.
        x and y can be coordinate modifier the the values returned.
        """
        topleft = self.rect.topleft
        if x or y:
            return (topleft[0]+x, topleft[1]+y)
        return topleft

    @property
    def absolute_collide_topleft(self):
        """Get the topleft absolute sprite position."""
        x,y = self.position
        rect = self.collide_rect
        return (x-rect.width/2, y-rect.height)

    @property
    def absolute_collide_bottomright(self):
        """Get the bottomright absolute sprite position."""
        x,y = self.position
        rect = self.collide_rect
        return (x+rect.width/2, y)

    @property
    def position_grid(self):
        """Return the position of the sprite on the gridmap of the level"""
        return self.currentLevel.toGridCoord(self.position)

    def isNearTo(self, point):
        """Check if the sprite collision rect (the basement) is near to a point.
        """
        # BBB: I'm using a majored version of the collide rect to fix a problem with a charas-bouncing-effect on movement... :-|
        x, y = self.currentLevel.transformToScreenCoordinate(point)
        collide_rect = self.collide_rect
        collide_rect.height+=3
        return collide_rect.collidepoint(x, y)

    def toScreenCoordinate(self):
        """Return (x,y) tuple information relative to the screen position"""
        return self.currentLevel.transformToScreenCoordinate(self.position)

    def toLevelCoordinate(self):
        """Return (x,y) tuple information in the absolute level coordinate, taken from the sprite rect"""
        return self.currentLevel.transformToLevelCoordinate(self.rect.midbottom)

    def getTip(self):
        """Get a tip to be printed near the character. Override this for subclass if you want this feature.
        You must return something false but not None (the default) if you don't have tip yet but wanna
        that this GameSprite gets subscribed to the tippable group.
        @return None or {'text':text, 'color':color, 'font':font, 'background':bkcolor}
        Font and background are optional.
        """
        return None

    def addToGameLevel(self, level, firstPosition):
        """Add this sprite to a level.
        You must set an initial position that become the midbottom position of the sprite rect.
        """
        self.currentLevel = level
        self.x, self.y = firstPosition
        rectPosition = level.transformToScreenCoordinate(firstPosition)
        self.rect.midbottom = rectPosition
        if isinstance(self, UniqueObject):
            cblocals.object_registry.register(self)

    def checkCollision(self, x, y, silent=False):
        """Check collision of this sprite with others taken from the 'physical' group.
        If a collision occurs, a SPRITE_COLLISION_EVENT is raised.
        @x, y: used to adjust the collire_rect before detection.
        @silent: default to False. If True, no event is raised on collision
        """
        # BBB: use of the zindex info can be useful here in future (flying characters)?
        x, y = utils.normalizeXY(x, y)
        collide_rect = self.collide_rect.move(x,y)
        collideGroups = (self.currentLevel['physical'],)
        for group in collideGroups:
            for sprite in group.sprites():
                if sprite is self:
                    continue
                if collide_rect.colliderect(sprite.collide_rect):
                    if not silent:
                        event = pygame.event.Event(cblocals.SPRITE_COLLISION_EVENT, {'source':self, 'to': sprite})
                        pygame.event.post(event)
                    return True
        return False

    @property
    def collide_rect(self):
        """Return a rect used for collision in movement. This must be equals to sprite "foot" area.
        For general GameSprite, the collide rect is the same as the rect attribute.
        You probably wanna (must) overwrite this in all subclasses!
        """
        return self.rect

    @property
    def physical_rect(self):
        """Return a rect used for collision (not collision with movement!)
        This must be equals to image's character total area.
        You probably wanna (must) overwrite this in all subclass!
        """
        return self.collide_rect

    @property
    def collide_grid(self):
        """Return the collide_rect infos in a format usable onto a GridMap instance.
        The sprite must be added to a GameLevel instance
        @return: list of blocked grid coordinates.
        """
        topleft = self.absolute_collide_topleft
        bottomright = self.absolute_collide_bottomright
        tlx, tly = self.currentLevel.toGridCoord(topleft)
        brx, bry = self.currentLevel.toGridCoord(bottomright)
        collide_grid = []
        for x in range(tlx, brx+1):
            for y in range(tly, bry+1):
                collide_grid.append( (x,y) )
        if not collide_grid:
            collide_grid = [(tlx,tly)]
        return collide_grid

    def distanceFrom(self, sprite):
        """Return the distance between this sprite and another one"""
        return Vector2.from_points(self.position,sprite.position).get_magnitude()

    def move(self, x, y):
        """Move the sprite, relative to current point"""
        self.x+=x
        self.y+=y

    @classmethod
    def generateEmptySprite(cls, size, alpha=None, fillWith=None, colorKey=None):
        """Return Surface. Default setting is for blank and not filled ones.
        You can enter alpha value, fill color and colorkey color for per-pixel-alpha.
        """
        # BBB: move this away from here, like in a simple module
        surface = pygame.Surface(size, flags=HWSURFACE|HWPALETTE, depth=32)
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

    def triggerCollision(self, source):
        """This method can be overrided in subclasses. Is called every time a sprite
        collide with this sprite.
        Source is the sprite that collide. Base implementation does nothing at all.
        """
        pass

    @classmethod
    def manageCollisions(cls, source, to):
        """Class method for handling collision by sprites.
        If the source "sprite" collide with the "to" sprite, the triggerCollision method is called
        onto the "to" sprite.
        """
        to.triggerCollision(source)
        logging.debug("%s sprite collided with %s" % (source, to))

    @property
    def outOfScreen(self):
        """True if the sprite is out of the screen coordinates"""
        x,y = self.currentLevel.transformToScreenCoordinate(self.position)
        w,h = cblocals.GAME_SCREEN_SIZE
        if x<0 or y<0 or x>x or y>h:
            return True
        return False

 