# -*- coding: utf-8 -

import logging

import pygame
from pygame.locals import *
from cheeseboys import cblocals, utils
from cheeseboys.utils import Vector2
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

    def update(self, time_passed):
        """Update method of pygame Sprite class.
        Keep updated sprite position on level.
        """
        pygame.sprite.Sprite.update(self, time_passed)
        self.refresh()

    def refresh(self):
        """Refresh sprite position based on x,y tuple"""
        x, y = self.toScreenCoordinate()
        self.rect.midbottom = (x, y)

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
        x,y = self.position_int
        rect = self.collide_rect
        return (x-rect.width/2, y-rect.height)

    @property
    def absolute_collide_bottomright(self):
        """Get the bottomright absolute sprite position."""
        x,y = self.position_int
        rect = self.collide_rect
        return (x+rect.width/2, y)

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
        return Vector2(self.position)

    @property
    def position_grid(self):
        """Return the position of the sprite on the gridmap of the level"""
        return self.currentLevel.toGridCoord(self.position_int)

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
        return self.currentLevel.transformToScreenCoordinate(self.position_int)

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

    def checkCollision(self, x, y):
        """Check collision of this sprite with others taken from the 'physical' group.
        Params x and y are used to adjust the collire_rect before detection.
        If a collision occurs, a SPRITE_COLLISION_EVENT is raised.
        """
        # BBB: use of the zindex info can be useful here in future?
        x, y = utils.normalizeXY(x, y)
        collide_rect = self.collide_rect.move(x,y)
        collideGroups = (self.currentLevel['physical'],)
        for group in collideGroups:
            for sprite in group.sprites():
                if sprite is self:
                    continue
                if collide_rect.colliderect(sprite.collide_rect):
                    event = pygame.event.Event(cblocals.SPRITE_COLLISION_EVENT, {'source':self, 'to': sprite})
                    pygame.event.post(event)
                    return True
        return False

    def getBestCoordinateToAvoidCollision(self, x, y):
        """This is a method similar to GameSprite.checkCollision.
        If a collision is found for this sprite at (x,y) offset from this position, then other modified coordinates like
        (x,0) or (0,y) are tested.
        Again, if a collision occurs, a SPRITE_COLLISION_EVENT is raised.
        @return A new free (x,y) tuple, or an empty one if no good free point is found.
        """
        x, y = utils.normalizeXY(x, y)
        collide_rect = self.collide_rect
        collide_coords = [(x,y), (x,0), (0,y)]
        collide_coords_registry = [True, True, True]
        collide_sprites = [None, None, None]
        collideGroups = (self.currentLevel['physical'],)
        for group in collideGroups:
            for sprite in group.sprites():
                if sprite is self:
                    continue
                cnt = 0
                for collide_coord in collide_coords:
                    rect = collide_rect.move(*collide_coord)
                    if collide_rect.colliderect(sprite.collide_rect):
                        # Mark coord as a bad ones
                        collide_sprites[cnt] = sprite
                        collide_coords_registry[cnt] = False
                    cnt+=1
        # Now I need to find the best one
        return self._choseBestOffset(collide_coords, collide_coords_registry, collide_sprites)

    def _choseBestOffset(self, collide_coords, collide_coords_registry, collide_sprites):
        """@return a tuple with be best coord I can choose. See GameSprite.getBestCoordinateToAvoidCollision"""
        if collide_coords_registry[0]:
            return collide_coords[0]
        if not collide_coords_registry[0] and not collide_coords_registry[1] and not collide_coords_registry[2]:
            # All coords are bad; a collision occurs
            event = pygame.event.Event(cblocals.SPRITE_COLLISION_EVENT, {'source':self, 'to': collide_sprites[0]})
            pygame.event.post(event)
            return ()
        if collide_coords_registry[1] and collide_coords_registry[2]:
            # I must chose point nearer to the target
            navPoint = self.navPoint
            base_position = self.position
            x,y = base_position
            x+= collide_coords[1][0]
            y+= collide_coords[1][1]
            magnitude1 = Vector2.from_points((x,y),navPoint.as_tuple()).get_magnitude()
            x,y = base_position
            x+= collide_coords[2][0]
            y+= collide_coords[2][1]
            magnitude2 = Vector2.from_points((x,y),navPoint.as_tuple()).get_magnitude()
            if magnitude1<=magnitude2:
                return collide_coords[1]
            else:
                return collide_coords[2]
        # At his line only one coord can be valid
        if collide_coords_registry[1]:
            return collide_coords[1]
        else:
            return collide_coords[2]

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
        for x in range(tlx, brx):
            for y in range(tly, bry):
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
        self.refresh()

    @classmethod
    def generateEmptySprite(cls, size, alpha=None, fillWith=None, colorKey=None):
        """Return Surface. Default setting is for blank and not filled ones.
        You can enter alpha value, fill color and colorkey color for per-pixel-alpha.
        """
        # BBB: move this away from here, like in a simple module
        surface = pygame.Surface(size, depth=32)
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

 