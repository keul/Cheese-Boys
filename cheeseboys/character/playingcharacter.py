# -*- coding: utf-8 -

import pygame
from pygame.locals import *

from cheeseboys import utils
from cheeseboys import cblocals
from cheeseboys.pygame_extensions.sprite import GameSprite
from cheeseboys.vector2 import Vector2
from character import Character

class PlayingCharacter(Character):
    """Human player character class"""

    def afterInit(self):
        self.side = "Veneto"
        self.experienceLevel = 2
        self._trackedEnemy = None
        self.attackDamage = "1d6+2"
        self.hitPoints = self.hitPointsLeft = 30
        self.rest_time_needed = .25
        self._speech.textcolor = (0,0,150,0)
        # stealth
        self.stealthLevel = 1
        self.stealthRestTimeNeeded = 3000
        # list of visible other character
        self.can_see_list = {}

    def update(self, time_passed):
        """Update method of pygame Sprite class.
        Overrided the one in Character main class because we need to handle user controls here.
        """
        GameSprite.update(self, time_passed)
        if cblocals.global_lastMouseLeftClickPosition or cblocals.global_lastMouseRightClickPosition:
            self.stopThinking()
        
        if self._brain.active_state and self._brain.active_state.name!="controlled":
            return Character.update(self, time_passed)
        
        pressed_keys = pygame.key.get_pressed()
        # update stealth level
        if pressed_keys[K_LSHIFT] and self.canStealthAgain() and not self.stealth:
            self.stealth = True
        elif not pressed_keys[K_LSHIFT] and self.stealth:
            self.stealth = False
        
        # Check for mouse actions setted
        if cblocals.global_lastMouseLeftClickPosition:
            self.navPoint.set(self.currentLevel.transformToLevelCoordinate(cblocals.global_lastMouseLeftClickPosition))
            cblocals.global_lastMouseLeftClickPosition = ()
        if cblocals.global_lastMouseRightClickPosition and not self.isAttacking():
            attackHeading = Vector2.from_points(self.position, self.currentLevel.transformToLevelCoordinate(cblocals.global_lastMouseRightClickPosition))
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

        if pygame.key.get_pressed()[K_z] and not self.stealth:
            self._brain.setState("retreat")

        if self.navPoint:
            self.moveBasedOnNavPoint(time_passed)
        
        if self._attackDirection:
            self.updateAttackState(time_passed)


    def _setSeeking(self, enemy):
        self._trackedEnemy = enemy
    seeking = property(lambda self: self._trackedEnemy, _setSeeking, doc="""The enemy that the hero is hunting""")
    
    def stopThinking(self):
        """Block all state machine brain actions of the hero, keeping back the control of him"""
        self._brain.setState("controlled")

    def moveBasedOnRetreatAction(self, time_passed):
        """See moveBasedOnRetreatAction of Character class.
        The playing character movement is based on the mouse position on the screen, but you can't retreat moving
        in front.
        """
        cpos = self.toScreenCoordinate()
        mpos = pygame.mouse.get_pos()
        toMouse = Vector2.from_points(cpos,mpos)
        toMouse.normalize()
        rheading = -toMouse
        
        heading = self.heading
        angle_between = heading.angle_between(rheading)
        if angle_between>=-30 and angle_between<=30:
            return
        
        distance = time_passed * self.speed
        movement = rheading * distance
        x = movement.get_x()
        y = movement.get_y()
        if not self.checkCollision(x, y) and self.checkValidCoord(x, y):
            self.move(x, y)

    def kill(self):
        """When playing character die all mouse pointer must be disabled"""
        Character.kill(self)
        cblocals.global_controlsEnabled = False

