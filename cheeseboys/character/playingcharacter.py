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
        Overrided the one in Character main class because we need to handle user controls here.
        """
        # 1. Check for mouse actions setted
        if locals.global_lastMouseLeftClickPosition:
            self.setNavPoint(*locals.global_lastMouseLeftClickPosition)
            locals.global_lastMouseLeftClickPosition = ()
        if locals.global_lastMouseRightClickPosition and not self.attackHeading:
            # Click of right button: stop moving and attack!
            self.attackHeading = Vector2.from_points(self.position, locals.global_lastMouseRightClickPosition)
            self.attackHeading.normalize()
            locals.global_lastMouseRightClickPosition = ()
            self.setAttackState(self.attackHeading)

        # 2. Keys movement
        pressed_keys = pygame.key.get_pressed()
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

        # BBB: if this is equal to update method of superclass, I can call it there!
        if self.navPoint:
            self._moveBasedOnNavPoint(time_passed)
        
        if self._attackDirection:
            self._updateAttackState(time_passed)


    
