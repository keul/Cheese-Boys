# -*- coding: utf-8 -

import pygame
from pygame.locals import *

import utils
import locals
from utils import Vector2
from character import Character

class PlayingCharacter(Character):
    """player character class"""
    
    def update(self, time_passed):
        """Update method of pygame Sprite class.
        Overrided the one in Character main class because we need to handle controls here.
        """
        pressed_keys = pygame.key.get_pressed()
        
        # 1. Check for mouse navPoint setted
        if locals.global_lastMouseLeftClickPosition and not self.navPoint or (self.navPoint and self.navPoint.as_tuple()!=locals.global_lastMouseLeftClickPosition):
            self.navPoint = Vector2(*locals.global_lastMouseLeftClickPosition)
            destination = self.navPoint # - Vector2(*self.image.get_size())/2.
            self.heading = Vector2.from_points(self.position, destination)
            self.heading.normalize()
            print self.heading
            direction = self._generateDirectionFromHeading(self.heading)
            self._checkDirectionChange(direction)
        
        # 2. Keys movement
        if pressed_keys[K_LEFT] or pressed_keys[K_RIGHT] or pressed_keys[K_UP] or pressed_keys[K_DOWN]:
            self.moving(True)
            self.navPoint = None
            locals.global_lastMouseLeftClickPosition = ()
            if pressed_keys[K_LEFT] and pressed_keys[K_UP]:
                direction = locals.DIRECTION_NW
            elif pressed_keys[K_LEFT] and pressed_keys[K_DOWN]:
                direction = locals.DIRECTION_SW
            elif pressed_keys[K_RIGHT] and pressed_keys[K_UP]:
                direction = locals.DIRECTION_NE
            elif pressed_keys[K_RIGHT] and pressed_keys[K_DOWN]:
                direction = locals.DIRECTION_SE
            elif pressed_keys[K_LEFT]:
                direction = locals.DIRECTION_W
            elif pressed_keys[K_RIGHT]:
                direction = locals.DIRECTION_E
            elif pressed_keys[K_UP]:
                direction = locals.DIRECTION_N
            elif pressed_keys[K_DOWN]:
                direction = locals.DIRECTION_S
            self.direction = direction
            distance = time_passed * self.speed
            self.walk(distance)
        elif self.navPoint:
            self.moving(True)
            distance = time_passed * self.speed
            movement = self.heading * distance
            self.addDistanceWalked(distance)
            self._x += movement.get_x()
            self._y += movement.get_y()
            self.refresh()
            if self.isNearTo(*self.navPoint.as_tuple()):
                locals.global_lastMouseLeftClickPosition = ()
                self.navPoint = None
                self.moving(False)



    
