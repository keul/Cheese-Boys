# -*- coding: utf-8 -*-

import pygame

__author__ = "Keul - lucafbb AT gmail.com"
__version__ = "0.1.0"

class KTextSurfaceWriter(object):
    """Generate a text displayed inside a given pygame.Rect.
    You can change/choose font size and color, and can fill the surface part.
    """
    
    def __init__(self, rect, font=None, color=(0,0,255,0), fillcolor=(0,0,0,0), justify_chars=0):
        self.rect = rect
        if not font:
            self.font = pygame.font.Font(None, 16)
        else:
            self.font = font
        self.fillcolor = fillcolor
        self.color = color
        self._text = "KTextSurfaceWriter - version %s" % __version__
        self._resultPage = []
        self.justify_chars = justify_chars
        self._mustClear = True
    
    def _setText(self, text):
        self._text = text
        self._resultPage = []
        self._mustClear = True
    text = property(lambda self: self._text, _setText, doc="""The text to be displayed""")

    @classmethod
    def normalizeTextLength(cls, text_too_long, font, max_length, justify_chars=0):
        """This function take a text too long and split it in a list of smaller text lines.
        The final text max length must be less/equals than max_length parameter, using the font passed.
        
        @return: a list of text lines.
        """
        words = [x for x in text_too_long.split(" ")]
        words_removed = []
        tooLong = True
        txt1 = txt2 = ""
        while tooLong:
            try:
                words_removed.append(words.pop())
            except IndexError:
                break
            txt1 = " ".join(words)
            if font.size(txt1)[0]<=max_length:
                tooLong = False
        words_removed.reverse()
        txt2 = (" "*justify_chars) + " ".join(words_removed)
        if txt2==text_too_long:
            # I cant split this line... I'll cut at the max wide
            while font.size(txt2)[0]>max_length:
                txt2 = txt2[:-1].strip()
        if font.size(txt2)[0]<=max_length:
            return [txt1, txt2]
        else:
            return [txt1] + cls.normalizeTextLength(txt2, font, max_length, justify_chars=justify_chars)

    def _getPreparedText(self):
        """Prepare text for future rendering.
        @return: a list of all lines to be drawn
        """
        if self._resultPage:
            return self._resultPage
        rw = self.rect.width
        rh = self.rect.height
        text = self.text
        resultPage = []
        for line in text.split("\n"):
            lw, lh = self.font.size(line)
            if lw>rw:
                newtextlines = self.normalizeTextLength(line, self.font, rw, justify_chars=self.justify_chars)
            else:
                newtextlines = [line,]
            resultPage.extend(newtextlines)
        self._resultPage = resultPage
        return resultPage

    def clear(self, surface, fillcolor=None):
        """Clear the subsurface with the fillcolor choosen"""
        if not fillcolor:
            fillcolor = self.fillcolor
        subs = surface.subsurface(self.rect)
        subs.fill(fillcolor)

    def draw(self, surface):
        """Draw the text to the surface."""
        if self._mustClear:
            self.clear(surface)
            self._mustClear = False
        resultPage = self._getPreparedText()
        rect = self.rect
        i = 0
        for line in resultPage:
            ren = self.font.render(line, 1, self.color, self.fillcolor)
            surface.blit(ren, (rect.left, rect.top + i*self.font.get_height()))
            i+=1