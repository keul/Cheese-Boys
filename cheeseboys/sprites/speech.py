# -*- coding: utf-8 -

import pygame
from pygame.locals import *
from cheeseboys.pygame_extensions import GameSprite
from cheeseboys import cblocals

CLOUD_MAX_WIDTH = 200
MAX_TEXTLINES = 5
PER_LINE_PADDING = 3
BORDER_PADDING = 5
T4WORD = 1

class SpeechCloud(GameSprite):
    """This sprite, done to be contained in the speech group with high zindex,
    is used by characters to speak, say something.
    """
    
    def __init__(self, character, bkcolor=(50,50,50,180), textcolor=(255,255,255)):
        GameSprite.__init__(self)
        self._character = character
        self.bkcolor = bkcolor
        self.textcolor = textcolor
        self._text = ""
        self._time_left = 0
        self._last_charX = self._last_charY = None
        self._image = None
    
    def initSpeech(self):
        character = self._character
        level = character.currentLevel
        self.rect = self._getRect()
        level['speech'].add(self)
        self._last_charX = self._last_charY = character.position_int
        self.addToGameLevel(level, firstPosition=self.rect.topleft)

    def _setText(self, text):
        self._image = None # break memoization
        if self._text:
            # Append text if needed
            self._text += "\n"
        else:
            self.initSpeech()
        self._updateTimeLeft(text)
        self._text += text
    text = property(lambda self: self._text, _setText, doc="""The text of the SpeechCloud""")

    def _getRect(self):
        """Calc the rect position"""
        speech_font = cblocals.speech_font
        speech_font_h = speech_font.get_height()
        textlines = self.text.split("\n")[:MAX_TEXTLINES]
        w = BORDER_PADDING + max( [speech_font.size(x)[0] for x in textlines] ) + BORDER_PADDING
        h = BORDER_PADDING + len(textlines)*speech_font_h + PER_LINE_PADDING*(len(textlines)-1) + BORDER_PADDING
        character = self._character
        text_posx, text_posy = character.rect.midtop
        rect = pygame.Rect( (text_posx-w/2,text_posy-15), (w,h) )
        return rect

    @property
    def image(self):
        if False and self._image:
            # memoize it
            return self._image
        self.rect = self._getRect()
        speech_font = cblocals.speech_font
        speech_font_h = speech_font.get_height()
        srf = self._loadEmptySprite(self.rect.size, alpha=170)
        srf.fill(self.bkcolor, self.rect)
        ptop = BORDER_PADDING
        for text_line in self.text.split("\n")[:MAX_TEXTLINES]:
            srf.blit(speech_font.render(text_line, True, self.textcolor), (BORDER_PADDING, ptop) )
            ptop += speech_font_h + PER_LINE_PADDING
        self._image = srf
        return srf
    
    def update(self, time_passed):
        """The update must do 2 task: follow the character and disappear after a while.
        The text remains visible some times, based on text length.
        """
        GameSprite.update(self, time_passed)
        self._time_left-= time_passed
        if self._time_left<=0:
            self._time_left=0
            self._text = ""
            self.kill()
    
    def _updateTimeLeft(self, text):
        """Base on text length, the _time_left member will be updated"""
        # BBB: the alghoritm here can be very silly
        words = text.split()
        self._time_left+= T4WORD * len(words)