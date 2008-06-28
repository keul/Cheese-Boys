# -*- coding: utf-8 -

import pygame
from pygame.locals import *

from cheeseboys import utils
from cheeseboys import cblocals
from cheeseboys.utils import Vector2
from character import Character

class PlayingCharacter(Character):
    """Player character class"""

    def afterInit(self):
        self.side = "Veneto"
        self._trackedEnemy = None

    def update(self, time_passed):
        """Update method of pygame Sprite class.
        Overrided the one in Character main class because we need to handle user controls here.
        """
        if cblocals.global_lastMouseLeftClickPosition or cblocals.global_lastMouseRightClickPosition:
            self.stopThinking()
        
        if self._brain.active_state and self._brain.active_state.name!="controlled":
            return Character.update(self, time_passed)
        
        # 1. Check for mouse actions setted
        if cblocals.global_lastMouseLeftClickPosition:
            self.setNavPoint(cblocals.global_lastMouseLeftClickPosition)
            cblocals.global_lastMouseLeftClickPosition = ()
        if cblocals.global_lastMouseRightClickPosition and not self.isAttacking():
            attackHeading = Vector2.from_points(self.position, cblocals.global_lastMouseRightClickPosition)
            attackHeading.normalize()
            cblocals.global_lastMouseRightClickPosition = ()
            # Right click on a distant enemy will move the hero towards him...
            if self.seeking:
                # enable the hero brain
                enemy = self.seeking
                print "Seeking %s" % enemy.name
                self.enemyTarget = enemy
                self._brain.setState("hunting")
            # ...or attack (even if moving)...
            else:
                self.setAttackState(attackHeading)

#        # 2. Keys movement
#        pressed_keys = pygame.key.get_pressed()
#        if pressed_keys[K_LEFT] or pressed_keys[K_RIGHT] or pressed_keys[K_UP] or pressed_keys[K_DOWN]:
#            self.moving(True)
#            self.navPoint = None
#            cblocals.global_lastMouseLeftClickPosition = ()
#            if pressed_keys[K_LEFT] and pressed_keys[K_UP]:
#                direction = cblocals.DIRECTION_NW
#            elif pressed_keys[K_LEFT] and pressed_keys[K_DOWN]:
#                direction = cblocals.DIRECTION_SW
#            elif pressed_keys[K_RIGHT] and pressed_keys[K_UP]:
#                direction = cblocals.DIRECTION_NE
#            elif pressed_keys[K_RIGHT] and pressed_keys[K_DOWN]:
#                direction = cblocals.DIRECTION_SE
#            elif pressed_keys[K_LEFT]:
#                direction = cblocals.DIRECTION_W
#            elif pressed_keys[K_RIGHT]:
#                direction = cblocals.DIRECTION_E
#            elif pressed_keys[K_UP]:
#                direction = cblocals.DIRECTION_N
#            elif pressed_keys[K_DOWN]:
#                direction = cblocals.DIRECTION_S
#            self.direction = direction
#            distance = time_passed * self.speed
#            self.walk(distance)

        if self.navPoint:
            self.moveBasedOnNavPoint(time_passed)
        
        if self._attackDirection:
            self.updateAttackState(time_passed)


    def _setSeeking(self, enemy):
        self._trackedEnemy = enemy
    seeking = property(lambda self: self._trackedEnemy, _setSeeking, doc="""The enemy that the hero is tracking""")
    
    def stopThinking(self):
        """Block all state machine brain actions of the hero, keeping back the control of him"""
        self._brain.setState("controlled")
