# -*- coding: utf-8 -

import pygame
from pygame.locals import *
from cheeseboys import cblocals
from cheeseboys.cblocals import LEVEL_TEXT_TYPE_NORMAL, LEVEL_TEXT_TYPE_BLACKSCREEN
from cheeseboys.pygame_extensions import GameSprite

V_DIFF = 30
H_DIFF = 50

BORDER_PADDING_H = 40
BORDER_PADDING_V = 20
PER_LINE_PADDING = 10

class LevelText(GameSprite):
    """Sprite that displaying a big popup window that contains text.
    Normally used by GameLevel method during presentations, or in game action for important information for the player.
    This sprite freese the game execution until the space bar is clicked.
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
            return pygame.Rect( (x,y), (sw, sh) )
        else:
            return pygame.Rect( (x+H_DIFF,y+V_DIFF), (sw-2*H_DIFF, sh-2*V_DIFF) ) 
    
    @property
    def image(self):
        if self._image:
            # memoized image
            return self._image
        if self._type == LEVEL_TEXT_TYPE_BLACKSCREEN:
            srf = self._loadEmptySprite(self.rect.size, alpha=255 , fillWith=(0,0,0))
        else:
            w,h = self.rect.size
            self.rect.move_ip(0,-V_DIFF)
            srf = self._loadEmptySprite( (w, h), alpha=200, fillWith=(0,0,0))
        text = cblocals.leveltext_font.render(self._text, True, (255,255,255))
        srf.blit(text, (BORDER_PADDING_H, BORDER_PADDING_V))
        self._image = srf
        return srf


    def update(self, time_passed):
        """Do nothing, but kill me when SPACE is hit"""
        GameSprite.update(self, time_passed)
        if pygame.key.get_pressed()[K_SPACE]:
            self.kill()