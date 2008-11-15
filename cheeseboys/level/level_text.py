# -*- coding: utf-8 -

import pygame
from pygame.locals import *
from cheeseboys import cblocals, utils
from cheeseboys.cblocals import LEVEL_TEXT_TYPE_NORMAL, LEVEL_TEXT_TYPE_BLACKSCREEN
from cheeseboys.pygame_extensions import GameSprite

# only used for non-fullscreen level text
V_DIFF = 30
H_DIFF = 50

BORDER_PADDING_H = 40
BORDER_PADDING_V = 20
LINE_HEIGHT_ADD = 8

COLOR_DEFAULT = (255, 255, 255)

class LevelText(GameSprite):
    """Sprite that displaying a big popup window that contains text.
    Normally used by GameLevel method during presentations, or in game action for important information for the player.
    This sprite freese the game execution until the space bar is clicked.
    """
    
    def __init__(self, level, text=None, type=LEVEL_TEXT_TYPE_NORMAL):
        GameSprite.__init__(self, level['level_text'])
        self._text = []
        self._type = type
        self.level = level
        self._image = None
        self.rect = self._getRect()
        if text:
            self.addText(text)
        self.colophon = False
    
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
            srf = self._loadEmptySprite( (w, h), alpha=220, fillWith=(0,0,0))
        
        for text, position, color in self._generatePage():
            text_to_display = cblocals.leveltext_font.render(_(text.decode('utf-8')), True, color)
            srf.blit(text_to_display, position)
        
        if self.colophon:
            bx,by = self.rect.bottomright
            srf.blit(utils.load_image('keul-software.png'), (bx-85,by-20) )
        
        self._image = srf
        return srf

    def update(self, time_passed):
        """Do nothing, but kill me when SPACE is hit"""
        GameSprite.update(self, time_passed)
        if pygame.key.get_pressed()[K_SPACE]:
            self.kill()

    def addText(self, text):
        """Add more text in a new line on this level text.
        Text can be a simple unicode string or a dictionary in the form:
        {'text': text_to_display, 'color': (r,g,b)}
        """
        self._image = None # memoization invalidation
        self._text.append(text)

    def _generatePage(self):
        """Starting from all stored text inside the instance, this method
        return a structure as this:
        [ (line_text, position, color), (...) ]
        The returned object can be looped for write the text on the screen;
        too long lines are automatically splitted in more line to fit
        LevelText dimension area.
        """
        outPage = []
        line_maxlength = self.rect.w - BORDER_PADDING_H*2
        y = BORDER_PADDING_V
        h = cblocals.leveltext_font.size("xxx")[1]
        for line in self._text:
            if type(line)!=dict:
                line_text = line
                line_color = COLOR_DEFAULT
            else: # dictionary
                line_text = line['text']
                line_color = line['color']
            w = cblocals.leveltext_font.size(line_text)[0]
            if w>line_maxlength:
                newtextlines = utils.normalizeTextLength(line_text, cblocals.leveltext_font, line_maxlength)
            else:
                newtextlines = [line_text,]
            newtextlines, y = self._preparePageLines(newtextlines, y, h, line_color)
            outPage.extend(newtextlines)
        return outPage
    
    def _preparePageLines(self, text_lines, y, h, line_color):
        """Given a list of text lines, prepare the structure as described in the _generatePage method.
        This method return a tuple with the structure and the new Y coordinated where start the next write.
        """
        newtextlines = []
        x = BORDER_PADDING_H
        for line in text_lines:
            newtextlines.append( (line, (x,y), line_color) )
            y+= h+LINE_HEIGHT_ADD
        return (newtextlines, y)

