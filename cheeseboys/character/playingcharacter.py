# -*- coding: utf-8 -

import pygame
from pygame.locals import *

import utils
from cheeseboys import cblocals
from utils import Vector2
from character import Character

class PlayingCharacter(Character):
    """player character class"""
    
    def update(self, time_passed):
        """Update method of pygame Sprite class.
        Overrided the one in Character main class because we need to handle user controls here.
        """
        # 1. Check for mouse actions setted
        if cblocals.global_lastMouseLeftClickPosition:
            self.setNavPoint(*cblocals.global_lastMouseLeftClickPosition)
            cblocals.global_lastMouseLeftClickPosition = ()
        if cblocals.global_lastMouseRightClickPosition and not self.isAttacking():
            # Click of right button: stop moving and attack!
            self.attackHeading = Vector2.from_points(self.position, cblocals.global_lastMouseRightClickPosition)
            self.attackHeading.normalize()
            cblocals.global_lastMouseRightClickPosition = ()
            self.setAttackState(self.attackHeading)

        # 2. Keys movement
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_LEFT] or pressed_keys[K_RIGHT] or pressed_keys[K_UP] or pressed_keys[K_DOWN]:
            self.moving(True)
            self.navPoint = None
            cblocals.global_lastMouseLeftClickPosition = ()
            if pressed_keys[K_LEFT] and pressed_keys[K_UP]:
                direction = cblocals.DIRECTION_NW
            elif pressed_keys[K_LEFT] and pressed_keys[K_DOWN]:
                direction = cblocals.DIRECTION_SW
            elif pressed_keys[K_RIGHT] and pressed_keys[K_UP]:
                direction = cblocals.DIRECTION_NE
            elif pressed_keys[K_RIGHT] and pressed_keys[K_DOWN]:
                direction = cblocals.DIRECTION_SE
            elif pressed_keys[K_LEFT]:
                direction = cblocals.DIRECTION_W
            elif pressed_keys[K_RIGHT]:
                direction = cblocals.DIRECTION_E
            elif pressed_keys[K_UP]:
                direction = cblocals.DIRECTION_N
            elif pressed_keys[K_DOWN]:
                direction = cblocals.DIRECTION_S
            self.direction = direction
            distance = time_passed * self.speed
            self.walk(distance)

        # BBB: if this is equal to update method of superclass, I can call it there!
        if self.navPoint:
            self._moveBasedOnNavPoint(time_passed)
        
        if self._attackDirection:
            self._updateAttackState(time_passed)


    
