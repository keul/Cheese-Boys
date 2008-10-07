# -*- coding: utf-8 -

import pygame
from pygame.locals import *
from cheeseboys import cblocals
from cheeseboys.cblocals import LEVEL_TEXT_TYPE_NORMAL, LEVEL_TEXT_TYPE_BLACKSCREEN
from cheeseboys.pygame_extensions import GameSprite

V_DIFF = 20
H_DIFF = 30

BORDER_PADDING_H = 40
BORDER_PADDING_V = 20
PER_LINE_PADDING = 10

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
        sw, sh = cblocals.GAME_SCREEN_SIZE
        if self._type==LEVEL_TEXT_TYPE_BLACKSCREEN:
            self.x = x+sw/2
            self.y = y+sh
            return pygame.Rect( (x,y), cblocals.GAME_SCREEN_SIZE)
        else:
            w,h = cblocals.GAME_SCREEN_SIZE
            self.x = x+sw/2
            self.y = y+sh - V_DIFF
            return pygame.Rect( (x+H_DIFF,y+V_DIFF), (w-2*H_DIFF, h-2*V_DIFF) ) 
    
    @property
    def image(self):
        if self._image:
            # memoized image
            return self._image
        if self._type == LEVEL_TEXT_TYPE_BLACKSCREEN:
            srf = self._loadEmptySprite(cblocals.GAME_SCREEN_SIZE, alpha=255 ,fillWith=(0,0,0))
            text = cblocals.leveltext_font.render(self._text, True, (255,255,255))
            srf.blit(text, (BORDER_PADDING_H, BORDER_PADDING_V))
        else:
            w,h = cblocals.GAME_SCREEN_SIZE
            w-= H_DIFF*2
            h-= V_DIFF*2
            srf = self._loadEmptySprite( (w,h), alpha=200, fillWith=(0,0,0))
            text = cblocals.leveltext_font.render(self._text, True, (255,255,255))
            srf.blit(text, (BORDER_PADDING_H, BORDER_PADDING_V))
        self._image = srf
        return srf


    def update(self, time_passed):
        """Do nothing, but kill me when SPACE is hit"""
        GameSprite.update(self, time_passed)
        if pygame.key.get_pressed()[K_SPACE]:
            self.kill()