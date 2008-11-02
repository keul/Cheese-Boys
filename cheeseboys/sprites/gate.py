# -*- coding: utf-8 -

import pygame
from pygame.locals import *
from cheeseboys.pygame_extensions import GameSprite
from cheeseboys import cblocals, utils

class Gate(GameSprite):
    """Gate sprite. Solid passage commonly closed.
    TODO: In future this will have an open/close animation.
    """
    
    def __init__(self, position, length, orientation, *containers):
        """Init the gate. Just give the length on the gate and the orientation.
        0 for horizontal, 1 for vertical.
        """
        GameSprite.__init__(self, *containers)
        self.length = length
        self.width = int(length/20)
        self.orientation = orientation
        self.rect = self._getRect(position, length, orientation)
        self._collide_rect = None
        self.position = position
        self.image = self._getImage()
        self.isOpen = False
        self._focus = False

    def _getRect(self, position, length, orientation):
        if orientation==0:
            rect = pygame.Rect( position, (length, length/2) )
        else:
            rect = pygame.Rect( position, (length/2, length) )
        return rect

    @property
    def collide_rect(self):
        """Collision rect of the gate; is where the gate is draw"""
        rect = self.rect
        if self.orientation==0:
            cr_rect = pygame.Rect( rect.topleft, (self.length,self.width) )
        else:
            cr_rect = pygame.Rect( rect.topleft, (self.width,self.length) )
        return cr_rect

    @property
    def physical_rect(self):
        """More thick than collide_rect because contains the open gate area"""
        rect = self.collide_rect
        if self.orientation==0:
            ph_rect = pygame.Rect( rect.topleft, (self.length,self.width*3) )
        else:
            ph_rect = pygame.Rect( rect.topleft, (self.width*3,self.length) )
        return ph_rect

    def _getImage(self):
        srf = self._loadEmptySprite(self.rect.size, colorKey=(0,0,0) )
        if self.orientation==0:
            rect = pygame.Rect( (0,0), (self.length,self.width) ) 
        else:
            rect = pygame.Rect( (0,0), (self.width,self.length) )
        pygame.draw.rect(srf, (100,255,100), rect, 0)
        return srf

    def update(self, time_passed):
        """TODO: open/close animation will be handled here"""
        GameSprite.update(self, time_passed)
        if cblocals.global_controlsEnabled:
            # Mouse curson
            if self.physical_rect.collidepoint(pygame.mouse.get_pos()):
                if not self._focus:
                    self.image.set_alpha(200)
                    utils.changeMouseCursor(cblocals.IMAGE_CURSOR_OPENDOOR_TYPE)
                    utils.drawCursor(cblocals.screen, pygame.mouse.get_pos())
                    self._focus = True
            else:
                if self._focus:
                    self.image.set_alpha(255)
                    if cblocals.global_mouseCursorType==cblocals.IMAGE_CURSOR_OPENDOOR_TYPE:
                        utils.changeMouseCursor(None)
                    self._focus = False

    def triggerCollision(self, source):
        """Override of the GameSprite.triggerCollision method.
        Do something only if the source is the hero!
        Open the gate, or say something if the hero can't
        """
        hero = self.currentLevel.hero
        if source is hero:
            hero.say("It wont open!", silenceFirst=True)

