# -*- coding: utf-8 -

import pygame
from pygame.locals import *
from cheeseboys.pygame_extensions.sprite import GameSprite
from cheeseboys import cblocals, utils
from cheeseboys.cbrandom import cbrandom

def randomTime():
    return cbrandom.uniform(.2, .4)


class Thunders(GameSprite):
    """Animation for a thunder effect.
    A demi-transparent surface that hide the screen content, and flash
    """
    
    def __init__(self, position, size, *containers):
        GameSprite.__init__(self, *containers)
        self.rect = pygame.Rect(position, size)
        self.x, self.y = position
        self.rect.midbottom = position
        self._image = None
        self._timeCollected = 0
        self._nextLightChange = randomTime()
        self._phase = 1

    @property
    def image(self):
        """Draw the flashing surfaces"""
        if self._image:
            # memoized image
            return self._image
        phase = self._phase
        if phase==1:
            self.currentLevel.shadow = False
            self._image = GameSprite.generateEmptySprite(self.rect.size, alpha=245, fillWith=(255,255,255))
            return self._image
        if phase==2:
            self._image = GameSprite.generateEmptySprite(self.rect.size, alpha=245, fillWith=(0,0,0))
            return self._image
        if phase==3:
            self._image = GameSprite.generateEmptySprite(self.rect.size, alpha=245, fillWith=(255,255,255))
            return self._image

    def update(self, time_passed):
        """Update method of pygame Sprite class.
        check if the image must be changed here.
        """
        GameSprite.update(self, time_passed)
        self._timeCollected+= time_passed
        if self._timeCollected>=self._nextLightChange:
            self._timeCollected = 0
            self._nextLightChange = randomTime()
            self._phase+=1
            self._image = None
            if self._phase==4:
                self.currentLevel.shadow = True
                self.kill()



class Lighting(GameSprite):
    """Animation for a lighting that strike the ground
    """
    
    def __init__(self, position, size, *containers):
        """The position used is the lighting strike point of the ground (midbottom)"""
        GameSprite.__init__(self, *containers)
        self.rect = pygame.Rect(position, size)
        self.x, self.y = position
        self.rect.midbottom = position
        self._image = None
        self._timeCollected = 0
        self._nextLightChange = randomTime()
        self._phase = 1

    @property
    def image(self):
        """Draw the 2 images of the lighting"""
        if self._image:
            # memoized image
            return self._image
        phase = self._phase
        if phase==1:
            self._image = utils.load_image('lighting1.png', directory='miscellaneous')
            return self._image
        if phase==2:
            self._image = utils.load_image('lighting2.png', directory='miscellaneous')
            return self._image

    def update(self, time_passed):
        """Update method of pygame Sprite class.
        Check if the image must be changed here.
        """
        GameSprite.update(self, time_passed)
        self._timeCollected+= time_passed
        if self._timeCollected>=self._nextLightChange:
            self._timeCollected = 0
            self._nextLightChange = randomTime()
            self._phase+=1
            self._image = None
            if self._phase==3:
                self.kill()

