# -*- coding: utf-8 -

import pygame
from pygame.locals import *
from cheeseboys.pygame_extensions.sprite import GameSprite
from cheeseboys import cblocals, utils

class LevelExit(GameSprite):
    """Important sprite that allow change of the level"""
    
    def __init__(self, position, size, exit_to, start_position, firstNavPoint, topleft, *containers):
        GameSprite.__init__(self, *containers)
        self.rect = pygame.Rect(position, size)
        self.image = self.generateEmptySprite(size, alpha=0, fillWith=(240,240,240))
        self._focus = False
        # Exit data
        self.to_level = exit_to
        self.start_position = start_position
        self.firstNavPoint = firstNavPoint
        self.nextTopleft = topleft

    def update(self, time_passed):
        """Update methods does:
        1) Check for mouse hover on the LevelExit area;
        if this is true, the sprite alpha value is changed and the area became a little visibile
        2) Check for hero movement on the exit. If this is true then raise the LEVEL_CHANGE_EVENT event
        """
        GameSprite.update(self, time_passed)
        if cblocals.global_controlsEnabled:
            # Mouse curson
            if self.physical_rect.collidepoint(pygame.mouse.get_pos()):
                if not self._focus:
                    self.image.set_alpha(50)
                    utils.changeMouseCursor(cblocals.IMAGE_CURSOR_CHANGELEVEL_TYPE)
                    utils.drawCursor(cblocals.screen, pygame.mouse.get_pos())
                    self._focus = True
            else:
                if self._focus:
                    self.image.set_alpha(0)
                    if cblocals.global_mouseCursorType==cblocals.IMAGE_CURSOR_CHANGELEVEL_TYPE:
                        utils.changeMouseCursor(None)
                    self._focus = False

            # Change level
            if self.to_level and self.physical_rect.colliderect(self.currentLevel.hero.physical_rect) and \
                        self.currentLevel.timeIn > 5.:
                event = pygame.event.Event(cblocals.LEVEL_CHANGE_EVENT, {'exit':self, })
                pygame.event.post(event)
    
    def getTip(self):
        """Tip of a level exit give info on where it lead but only when mouse hover on it.
        """
        if self._focus:
            tip = self._emptyTipStructure.copy()
            tip['text']=self.to_level or "???"
            tip['background']=(255,255,255)
            return tip
        return ""

