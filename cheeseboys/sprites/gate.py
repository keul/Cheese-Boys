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
        
        To open the gate set the open_condition attribute.
        The open_condition must be evaluated to True, or must be a callable that return True.
        In any one of this case, the gate will open on collision with the hero.
        """
        GameSprite.__init__(self, *containers)
        self.length = self.total_length = length
        self.width = int(length/20)
        self.orientation = orientation
        self.position = position
        self._initGate()
        self.opened = False
        self.isOpen = False
        self._focus = False
        self.open_condition = None
        # Negate condition for opening
        self.open_condition_reverse_flag = False

    def _initGate(self):
        self.rect = self._getRect(self.position, self.total_length, self.orientation)
        self.image = self._getImage()

    def _getImage(self):
        srf = self._loadEmptySprite(self.rect.size, colorKey=(0,0,0) )
        if self.orientation==0:
            rect = pygame.Rect( (0,0), (self.length,self.width) ) 
        else:
            rect = pygame.Rect( (0,0), (self.width,self.length) )
        pygame.draw.rect(srf, (100,255,100), rect, 0)
        return srf

    def _getRect(self, position, length, orientation):
        if orientation==0:
            rect = pygame.Rect( position, (length, length/2) )
        else:
            rect = pygame.Rect( position, (length/2, length) )
        return rect

    def open(self):
        """Open the gate"""
        self.length = int(self.length/3)
        self._initGate()
        self.opened = True

    def close(self):
        """Close the gate"""
        self.length = self.length*3
        self._initGate()
        self.opened = False

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
            ph_rect = pygame.Rect( rect.topleft, (self.total_length,self.width*3) )
        else:
            ph_rect = pygame.Rect( rect.topleft, (self.width*3,self.total_length) )
        return ph_rect

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
        open_condition = self.open_condition
        open_condition_reverse_flag = self.open_condition_reverse_flag
        if source is hero and not self.opened:
            cond = True
            if open_condition_reverse_flag:
                cond=False
            if open_condition is not None:
                # TODO: fix this!
                if (type(open_condition)==bool and open_condition==cond) or \
                            (type(open_condition)!=bool and open_condition()==cond):
                    self.open()
                    return
            hero.say("It wont open!", silenceFirst=True)

