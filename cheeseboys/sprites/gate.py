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
        self.position = position
        self.image = self._getImage()
        self.isOpen = False

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
        if self.orientation:
            cr_rect = pygame.Rect( rect.topleft, (self.width,self.length) )
        else:
            cr_rect = pygame.Rect( rect.topleft, (self.length,self.width) )        
        return cr_rect

    def _getImage(self):
        srf = self._loadEmptySprite(self.rect.size, colorKey=(0,0,0) )
        if self.orientation:
            rect = pygame.Rect( (0,0), (self.width,self.length) )
        else:
            rect = pygame.Rect( (0,0), (self.length,self.width) ) 
        pygame.draw.rect(srf, (100,255,100), rect, 0)
        return srf

    def update(self, time_passed):
        """TODO: open/close animation will be handled here"""
        GameSprite.update(self, time_passed)
