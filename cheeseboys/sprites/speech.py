# -*- coding: utf-8 -

import pygame
from pygame.locals import *
from cheeseboys.pygame_extensions import GameSprite
from cheeseboys import cblocals

CLOUD_MAX_WIDTH = 200
T4WORD = 1

class SpeechCloud(GameSprite):
    """This sprite, done to be contained in the speech group with high zindex,
    is used by characters to speak, say something.
    """
    
    def __init__(self, character, bkcolor=(0,0,0,180), textcolor=(255,255,255)):
        GameSprite.__init__(self)
        self._character = character
        self.bkcolor = bkcolor
        self.textcolor = textcolor
        self._text = ""
        self._time_left = 0
    
    def initSpeech(self):
        level = self._character.currentLevel
        self.rect = self._getRect()
        level['speech'].add(self)
        self.addToGameLevel(level, firstPosition=self.rect.topleft)

    def _setText(self, text):
        if self._text:
            # Append text if needed
            self._text += "\n"
        else:
            self.initSpeech()
        self._updateTimeLeft(text)
        self._text += text
    text = property(lambda self: self._text, _setText, doc="""The text of the SpeechCloud""")

    def _getRect(self):
        """Calc the first rect position"""
        character = self._character
        text_posx, text_posy = character.position_int
        rect = pygame.Rect( (text_posx-30,text_posy-100 ), (CLOUD_MAX_WIDTH,100) )
        return rect

    @property
    def image(self):
        rect = self.rect
        srf = self._loadEmptySprite(rect.size, alpha=200)
        srf.fill(self.bkcolor, rect)
        srf.blit(cblocals.speech_font.render(self.text, True, self.textcolor), (2,0) )
        return srf
    
    def update(self, time_passed):
        """The update must do 2 task: follow the character and disappear after a while.
        The text remains visible some times, based on text length.
        """
        GameSprite.update(self, time_passed)
        self._time_left-= time_passed
        print self.rect.topleft, self.rect.size
        if self._time_left<=0:
            self._time_left=0
            self._text = ""
            self.kill()
    
    def _updateTimeLeft(self, text):
        """Base on text length, the _time_left member will be updated"""
        # BBB: the alghoritm here can be very silly
        words = text.split()
        self._time_left+= T4WORD * len(words)