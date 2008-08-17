# -*- coding: utf-8 -

import pygame
from pygame.locals import *

from cheeseboys.cbrandom import cbrandom

class Rain(object):
    """Even if this class is in the sprites module, the rain effects isn't a real pygame.Sprite type.
    Rain is drawn by using primitive pygame.draw functions.
    
    The rain is based only on screen coordinates and don't need to be transformed in level coordinate.

    Every raindrop is stored in this object within a structure like this:
    {'position': upper_position_tuple, 'speed':drop_speed, 'length': raindrop_length, 'width': raindrop_width}.
    
    Develop note: I'm not using the Vector2 class in there, because I wanna keep thing simple. This effect can became
    very speedkiller.
    """
    
    def __init__(self, surface_size):
        self._surface_size = surface_size
        self._rain_heading = (0,1)
        self._wind = -.1
        self._color = (187, 187, 187)
        self._raindrops = [
               {'position': (200, -50), 'speed': 500, 'length': 50, 'width': 1},
            ]

    def _getRaindropEndPosition(self, raindrop):
        """Use infos of a single raindrop to know the end point to be drawn on the screen"""
        start_position = raindrop['position']
        length = raindrop['length']
        rain_heading = (self._rain_heading[0]+self._wind, self._rain_heading[1])
        movementx, movementy = (rain_heading[0] * length, rain_heading[1] * length)
        return (raindrop['position'][0]+movementx, raindrop['position'][1]+movementy)

    def _generateRaindrop(self, raindrop=None, totallyRandom=False):
        """Generate a raindrop, changing the raindrop position or generating a new one.
        Use the totallyRandom if you don't want to generate the raindrop outside the screen.
        """
        pass

    def draw(self, surface):
        for raindrop in self._raindrops:
            pygame.draw.line(surface,
                             self._color,
                             raindrop['position'],
                             self._getRaindropEndPosition(raindrop),
                             raindrop['width'])
            #print raindrop['position']

    def update(self, time_passed):
        """Update the raindrops"""
        surface_size = self._surface_size
        for raindrop in self._raindrops:
            distance = time_passed * raindrop['speed']
            rain_heading = (self._rain_heading[0]+self._wind, self._rain_heading[1])
            movementx, movementy = (rain_heading[0] * distance, rain_heading[1] * distance)
            raindrop['position'] = (raindrop['position'][0]+movementx, raindrop['position'][1]+movementy)
            if raindrop['position'][1]+raindrop.length > surface_size[1]:
                self._generateRaindrop(raindrop, totallyRandom=False)