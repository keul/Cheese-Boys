# -*- coding: utf-8 -

import pygame
from pygame.locals import *
from cheeseboys.pygame_extensions import GameSprite
from cheeseboys import cblocals, utils

CLOUD_MAX_WIDTH = 250
MAX_TEXTLINES = 5
MIN_SPEECH_TIME = 2
MAX_SPEECH_TIME = 20
PER_LINE_PADDING = 3
BORDER_PADDING = 5
T4WORD = 1

class SpeechCloud(GameSprite):
    """This sprite, done to be contained in the speech group with high zindex,
    is used by characters to speak, say something.
    Is rendered on the screen as a box containing text speech.
    """
    
    def __init__(self, character, bkcolor=(255,255,255), textcolor=(0,0,0)):
        GameSprite.__init__(self)
        self._character = character
        self.bkcolor = bkcolor
        self.textcolor = textcolor
        self._text = ""
        self._text_queue = []
        self._time_left = 0
        self._last_charX = self._last_charY = None
        self._image = None
    
    def initSpeech(self):
        character = self._character
        level = character.currentLevel
        self.rect = self._getRect()
        level['speech'].add(self)
        self._last_charX = self._last_charY = character.position_int
        self.addToGameLevel(level, firstPosition=level.transformToLevelCoordinate(self.rect.midbottom))

    def _setText(self, text):
        """Setter of the text property.
        Text is always appended to text already existing.
        """
        self._image = None # break memoization
        if self._text:
            # Append text if needed
            self._text_queue.append(text)
        else:
            self.initSpeech()
            self._text = text
            self._updateTimeLeft(text)
    text = property(lambda self: self._text, _setText, doc="""The text of the SpeechCloud""")

    def additionalTime(self, additional_time):
        """Add some more time to the speech display time"""
        self._time_left+=additional_time

    @classmethod 
    def _generateTextLines(cls, text):
        """Generate text to be displayed, but return it splitted in a list at every line break.
        Also, if a line is too long (longer than CLOUD_MAX_WIDTH constant) the line itself is
        splitted again.
        """
        speech_font = cblocals.speech_font
        textlines = text.split("\n")[-MAX_TEXTLINES:]
        w = BORDER_PADDING + max( [speech_font.size(x)[0] for x in textlines] ) + BORDER_PADDING
        if w<CLOUD_MAX_WIDTH:
            return textlines
        # I've a problem, one or more lines are too long.
        newtextlines = []
        for line in textlines:
            w = BORDER_PADDING + speech_font.size(line)[0] + BORDER_PADDING
            if w>CLOUD_MAX_WIDTH:
                newtextlines.extend(utils.normalizeTextLength(line, speech_font, CLOUD_MAX_WIDTH-BORDER_PADDING*2))
            else:
                newtextlines.append(line)
        return newtextlines[-MAX_TEXTLINES:]

    def _getRect(self):
        """Return the right rect size for current text to show"""
        speech_font = cblocals.speech_font
        speech_font_h = speech_font.get_height()
        textlines = self._generateTextLines(self.text)
        w = BORDER_PADDING + max( [speech_font.size(x)[0] for x in textlines] ) + BORDER_PADDING
        h = BORDER_PADDING + len(textlines)*speech_font_h + PER_LINE_PADDING*(len(textlines)-1) + BORDER_PADDING
        character = self._character
        text_posx, text_posy = character.rect.midtop
        rect = pygame.Rect( (text_posx-w/2,text_posy-15-h), (w,h) )
        # Check valid coord in screen
        if rect.topleft[0]<0: rect.left = 0
        elif rect.topright[0]>cblocals.GAME_SCREEN_SIZE[0]: rect.right = cblocals.GAME_SCREEN_SIZE[0]
        if rect.topleft[1]<0: rect.top = 0
        elif rect.bottomleft[1]>cblocals.GAME_SCREEN_SIZE[1]: rect.bottom = cblocals.GAME_SCREEN_SIZE[1]
        return rect

    @property
    def image(self):
        """The image of this sprite is a pygame.Surface.
        Its a demi-transparent box with text inside that follow the character.
        """
        # BBB: memoization is disabled
        if False and self._image:
            # memoize it
            return self._image
        self.rect = self._getRect()
        speech_font = cblocals.speech_font
        speech_font_h = speech_font.get_height()
        srf = self.generateEmptySprite(self.rect.size, alpha=200, fillWith=self.bkcolor)
        ptop = BORDER_PADDING
        for text_line in self._generateTextLines(self.text):
            srf.blit(speech_font.render(text_line, True, self.textcolor), (BORDER_PADDING, ptop) )
            ptop += speech_font_h + PER_LINE_PADDING
        self._image = srf
        return srf
    
    def update(self, time_passed):
        """The update must do 2 task: follow the character and disappear after a while.
        The text remains visible some times, based on text length.
        """
        GameSprite.update(self, time_passed)
        self.position = self.currentLevel.transformToLevelCoordinate(self.rect.midbottom)
        self._time_left-= time_passed
        if self._time_left<=0:
            self.endSpeech()

    def endSpeech(self):
        """Terminate currently running speech"""
        self._time_left=0
        try:
            text = self._text_queue.pop(0)
            self._text = text
            self._updateTimeLeft(text)
        except IndexError:
            self._text = ""
            self.kill()

    def _updateTimeLeft(self, text):
        """Base on text length, the _time_left member of this object will be updated"""
        # BBB: the alghoritm here can be very silly
        words = text.split()
        self._time_left+= T4WORD * len([w for w in words if len(w)>3])
        if self._time_left>MAX_SPEECH_TIME:
            self._time_left=MAX_SPEECH_TIME
        elif self._time_left<MIN_SPEECH_TIME:
            self._time_left=MIN_SPEECH_TIME


