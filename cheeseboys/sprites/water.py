# -*- coding: utf-8 -

import pygame
from pygame.locals import *
from cheeseboys.pygame_extensions import GameSprite
from cheeseboys import cblocals, utils
from cheeseboys.cbrandom import cbrandom

class WaterWave(GameSprite):
    """Animation to be used on water background.
    This will draw a wave effects.
    """
    
    def __init__(self, position, dimension, *containers):
        GameSprite.__init__(self, *containers)
        self.rect = pygame.Rect(position, dimension)
        self._image = None
        self._wave_phase = 0
        self._timeCollected = self._nextRandomWaveTime()

    def _nextRandomWaveTime(self):
        """Return a time value. After this the wave image will be changed"""
        return cbrandom.uniform(0.7, 1.5)

    @property
    def image(self):
        """Draw an image of the wave; image will change with time"""
        if self._image:
            # memoized image
            return self._image
        wave_phase = self._wave_phase
        if wave_phase==0:
            self._image = utils.load_image("water-wave1.png", "miscellaneous")
            self._wave_phase = 1
            return self._image
        if wave_phase==1:
            self._image = utils.load_image("water-wave2.png", "miscellaneous")
            self._wave_phase = 2            
            return self._image
        if wave_phase==2:
            self._image = self._loadEmptySprite(self.rect.size)
            self._wave_phase = 0
            return self._image

    def update(self, time_passed):
        """Update method of pygame Sprite class.
        check if the image must be changed here.
        """
        GameSprite.update(self, time_passed)
        self._timeCollected-= time_passed
        if self._timeCollected<=0:
            self._timeCollected = self._nextRandomWaveTime()
            self._image = None
        