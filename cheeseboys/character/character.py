# -*- coding: utf-8 -

import random

import pygame
from pygame.locals import *

import utils
import locals
from utils import Vector2
from sprite import GameSprite

class Character(GameSprite):
    """Base character class"""
    
    def __init__(self, name, img, containers, firstPos=(100.,100.), speed=150., weaponInAndOut=False):
        
        GameSprite.__init__(self, *containers)
        self.containers = containers
        self.name = name
        self.img = img
        self._imageDirectory = "charas"
        
        self._load_images(img, weaponInAndOut)
        self.lastUsedImage = 'head_east_1'

        self._distanceWalked = 0
        self._mustChangeImage = False
        self.direction = self._lastUsedDirection = locals.DIRECTION_E
        self._attackDirection = None
        self._isMoving = False
        self.speed = speed
        
        self.navPoint = None
        self.heading =  None
        self.attackHeading = None
        
        self.dimension = locals.TILE_IMAGE_DIMENSION

        self._x = firstPos[0]
        self._y = firstPos[1]
        self.rect = self.image.get_rect(topleft = (100, 100))

    def getTip(self):
        """Print a tip text near the character"""
        rendered = locals.default_font.render(self.name, True, (255, 255, 255))
        return rendered

    def _load_images(self, img, weaponInAndOut):
        """Load images for this charas: 12 or 24 if used weaponInAndOut (so we need extra images without weapon)"""
        self.images = {}
        directory = self._imageDirectory
        if not weaponInAndOut:
            # 12 images
            self.images['walk_north_1'], self.images['head_north'], self.images['walk_north_2'], self.images['walk_east_1'], \
                self.images['head_east'], self.images['walk_east_2'], self.images['walk_south_1'], self.images['head_south'], \
                self.images['walk_south_2'], self.images['walk_west_1'], self.images['head_west'], \
                self.images['walk_west_2'] = utils.load_image(img, directory, charasFormatImage=True, weaponInAndOut=weaponInAndOut)
        else:
            # 24 images
            self.images['walk_north_1'], self.images['head_north'], self.images['walk_north_2'], self.images['walk_east_1'], \
                self.images['head_east'], self.images['walk_east_2'], self.images['walk_south_1'], self.images['head_south'], \
                self.images['walk_south_2'], self.images['walk_west_1'], self.images['head_west'], \
                self.images['walk_west_2'], \
                self.images['attack_north_1'], self.images['head_attack_north'], self.images['attack_north_2'], self.images['attack_east_1'], \
                self.images['head_attack_east'], self.images['attack_east_2'], self.images['attack_south_1'], self.images['head_attack_south'], \
                self.images['attack_south_2'], self.images['attack_west_1'], self.images['head_attack_west'], \
                self.images['attack_west_2'] = utils.load_image(img, directory, charasFormatImage=True, weaponInAndOut=weaponInAndOut)
                
    def update(self, time_passed):
        """Update method of pygame Sprite class.
        Non playing character check if has navPoint.
        """
        if self.navPoint:
            self._moveBasedOnNavPoint(time_passed)
        else:
            # no navPoint? For now move to a random direction
            self.setNavPoint(random.randint(1,639), random.randint(1,439) )

    def _moveBasedOnNavPoint(self, time_passed):
        """Common method for move character using navPoint infos"""
        destination = self.navPoint # - Vector2(*self.image.get_size())/2.
        self.heading = Vector2.from_points(self.position, destination)
        self.heading.normalize()
        direction = self._generateDirectionFromHeading(self.heading)
        self._checkDirectionChange(direction)

        self.moving(True)
        distance = time_passed * self.speed
        movement = self.heading * distance
        self.addDistanceWalked(distance)
        self._x += movement.get_x()
        self._y += movement.get_y()
        self.refresh()
        if self.isNearTo(*self.navPoint.as_tuple()):
            self.navPoint = None
            self.moving(False)

    def _setX(self, newx):
        self._x = newx
    x = property(lambda self: self.rect.centerx, _setX, doc="""The character X position""")

    def _setY(self, newy):
        self._y = newy
    y = property(lambda self: self.rect.bottom-3, _setY, doc="""The character Y position""")

    @property
    def position(self):
        """Character position as tuple"""
        return (self.x, self.y)
    @property
    def position_int(self):
        """Same as position but in integer format"""
        return (int(self.x), int(self.y))
    
    def isNearTo(self, x, y):
        """Check in the character is near to a point"""
        return self.rect.collidepoint(x, y)
    
    @property
    def image(self):
        """Sprite must have an image property.
        In this way I can control what image return.
        """
        if self._isMoving:
            # I'm on moving
            if self._mustChangeImage:
                self._mustChangeImage = False
                image = self._getImageFromDirectionWalked(self._lastUsedDirection)
                self.lastUsedImage = image
            return self.images[self.lastUsedImage]
        else:
            # Stand and wait
            if self._attackDirection:
                direction = self._attackDirection
                weaponOut = True
            else:
                direction = self._lastUsedDirection
                weaponOut = False
            image = self._getImageFromDirectionFaced(direction, weaponOut)
            self.lastUsedImage = image
            return self.images[image]

    def _generateDirectionFromHeading(self, new_heading):
        """Looking at heading, generate a valid direction string"""
        # print new_heading
        x, y = new_heading.as_tuple()
        if abs(x)<.30 and y<0:
            return locals.DIRECTION_N
        if abs(x)<.30 and y>0:
            return locals.DIRECTION_S
        if x<0:
            return locals.DIRECTION_W
        return locals.DIRECTION_E
        # BBB

    def _getWalkImagePrefix(self, direction):
        if direction==locals.DIRECTION_E or direction==locals.DIRECTION_NE or direction==locals.DIRECTION_SE:
            return "walk_east_"
        if direction==locals.DIRECTION_W or direction==locals.DIRECTION_NW or direction==locals.DIRECTION_SW:
            return "walk_west_"
        if direction==locals.DIRECTION_N:
            return "walk_north_"
        if direction==locals.DIRECTION_S:
            return "walk_south_"     
        raise ValueError("Invalid direction %s" % direction)   
    
    def _getImageFromDirectionWalked(self, direction):
        """Using a direction taken get the right image name to display.
        This method check if an attack is currently executed by this character. If this is True
        we must return the image facing direction attacked
        """
        imagePrefix = self._getWalkImagePrefix(direction)
        if self.lastUsedImage.startswith(imagePrefix):
            if self.lastUsedImage.endswith("1"):
                image = self.lastUsedImage[:-1]+"2"
            else:
                image = self.lastUsedImage[:-1]+"1"
        else:
            image = imagePrefix+"1"
        return image

    def _getImageFromDirectionFaced(self, direction, weaponOut):
        """Using a direction, chose the right character non-moving image.
        Use weaponOut to know if an image without weapong carried must be used.
        """
        if direction==locals.DIRECTION_E or direction==locals.DIRECTION_NE or direction==locals.DIRECTION_SE:
            if weaponOut:
                image = "head_attack_east"
            else:
                image = "head_east"
        elif direction==locals.DIRECTION_W or direction==locals.DIRECTION_NW or direction==locals.DIRECTION_SW:
            if weaponOut:
                image = "head_attack_west"
            else:
                image = "head_west"
        elif direction==locals.DIRECTION_N:
            if weaponOut:
                image = "head_attack_north"
            else:
                image = "head_north"
        elif direction==locals.DIRECTION_S:
            if weaponOut:
                image = "head_attack_south"
            else:
                image = "head_south"     
        else:
            raise ValueError("Invalid direction %s" % direction) 
        return image

    def addDistanceWalked(self, distance):
        self._distanceWalked+=distance
        # Every MIN_PX_4_IMAGES_CHANGEpx change image to simulate footsteps.
        if self._distanceWalked>=locals.MIN_PX_4_IMAGES_CHANGE:
            #self._isMoving = False
            self._distanceWalked=0
            self._mustChangeImage = True
    
    def move(self, x, y):
        """Move the character, relative to current point"""
        self._x+=x
        self._y+=y
        #self.rect.move_ip(x, y)
        self.refresh()
    
    def refresh(self):
        """Refresh character position"""
        self.rect.x = self._x
        self.rect.y = self._y
        #screenrect = Rect(0, 0, locals.SCREEN_WIDTH, locals.SCREEN_HEIGHT)
        #self.rect.clamp_ip(screenrect)

    def _checkDirectionChange(self, direction):
        """Check if the character movement direction is changed"""
        if direction!=self._lastUsedDirection:
            self._lastUsedDirection = direction
            self._mustChangeImage = True

    def walk(self, distance, direction=None):
        """Walk the character to a direction"""
        if not direction:
            direction = self.direction
        if not self._isMoving:
            return
        
        self.addDistanceWalked(distance)
        self._checkDirectionChange(direction)

        if direction==locals.DIRECTION_E:
            self.move(distance, 0)
        elif direction==locals.DIRECTION_S:
            self.move(0, distance)
        elif direction==locals.DIRECTION_W:
            self.move(-distance,0)
        elif direction==locals.DIRECTION_N:
            self.move(0, -distance)
        elif direction==locals.DIRECTION_NE:
            self.move(distance, -distance)
        elif direction==locals.DIRECTION_SE:
            self.move(distance, distance)
        elif direction==locals.DIRECTION_SW:
            self.move(-distance, distance)
        elif direction==locals.DIRECTION_NW:
            self.move(-distance, -distance)

    def attacking(self, heading):
        """Set the character attack versus an heading direction.
        For duration of the attack the character can still moving, but will face the direction attacked.
        """
        direction = self._generateDirectionFromHeading(heading)
        self._attackDirection = direction
        self._mustChangeImage = True

    def moving(self, new_move_status):
        """Change character movement status"""
        if new_move_status!=self._isMoving:
            self._mustChangeImage = True
        self._isMoving = new_move_status

    def setNavPoint(self, x, y):
        """Set a new target navPoint for current character"""
        self.navPoint = Vector2(x, y)