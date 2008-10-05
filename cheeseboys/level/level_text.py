# -*- coding: utf-8 -

import pygame
from pygame.locals import *
from cheeseboys import cblocals
from cheeseboys.cblocals import LEVEL_TEXT_TYPE_NORMAL, LEVEL_TEXT_TYPE_BLACKSCREEN
from cheeseboys.pygame_extensions import GameSprite

V_DIFF = 20
H_DIFF = 30

class LevelText(GameSprite):
    """Sprite that displaying a big popup window that contains text.
    Normally used by GameLevel method during presentations.
    """
    
    def __init__(self, text, level, type=LEVEL_TEXT_TYPE_NORMAL):
        GameSprite.__init__(self, level['level_text'])
        self._text = text
        self._type = type
        self.level = level
        self._image = None
        self.rect = self._getRect()
    
    def _getRect(self):
        x,y = self.level.topleft
        sw, sh = cblocals.SCREEN_SIZE
        self.x = x+sw/2
        self.y = y+sh
        if self._type==LEVEL_TEXT_TYPE_BLACKSCREEN:
            return pygame.Rect( (x,y), cblocals.SCREEN_SIZE)
        else:
            w,h = cblocals.SCREEN_SIZE
            return pygame.Rect( (x+H_DIFF,y+V_DIFF), (w-H_DIFF, h-V_DIFF) ) 
    
    @property
    def image(self):
        if self._image:
            # memoized image
            return self._image
        if self._type == LEVEL_TEXT_TYPE_BLACKSCREEN:
            srf = self._loadEmptySprite(cblocals.SCREEN_SIZE, alpha=255 ,fillWith=(0,0,0))
            text = cblocals.leveltext_font.render(self._text, True, (155,155,155))
            srf.blit(text, (0,0))
        else:
            w,h = cblocals.SCREEN_SIZE
            w-= H_DIFF*2
            h-= V_DIFF*2
            srf = self._loadEmptySprite( (w,h), alpha=200, fillWith=(0,0,0))
            text = cblocals.leveltext_font.render(self._text, True, (155,155,155))
            srf.blit(text, (w,h))
        self._image = srf
        return srf


    def update(self, time_passed):
        """Do nothing, but kill me when SPACE is hit"""
        GameSprite.update(self, time_passed)
        if pygame.key.get_pressed()[K_SPACE]:
            self.kill()