# -*- coding: utf-8 -

import logging

import pygame
from pygame.locals import *

from cheeseboys.cbrandom import cbrandom

AVERAGE_RAINDROPS = 50
MAX_RAINDROPS = 100

class Rain(object):
    """Even if this class is in the sprites module, the rain effects isn't a real pygame.Sprite type.
    Rain is drawn by using primitive pygame.draw functions.
    
    The rain is based only on screen coordinates and don't need to be transformed in level coordinate.

    Every raindrop is stored in this object within a structure like this:
    {'position': upper_position_tuple, 'speed':drop_speed, 'length': raindrop_length, 'width': raindrop_width}.
    In any case use the class member emptyRainDrop
    
    Develop note: I'm not using the Vector2 class in there, because I wanna keep thing simple. This effect can became
    very speedkiller.
    """
    
    def __init__(self, surface_size, ndrops=AVERAGE_RAINDROPS):
        self._surface_size = surface_size
        self._rain_heading = (0,1)
        self._wind = -.1
        self._color = (187, 187, 187)
        self._raindrops = []
        for x in xrange(ndrops):
            self._raindrops.append(self._generateRaindrop(totallyRandom=True))
        for x in xrange(ndrops,MAX_RAINDROPS):
            self._raindrops.append(None)
        self._raindrops_length = ndrops
        self._time_rain_frequency = 0
        self._time_wind_strength = 0
        

    @property
    def emptyRainDrop(self):
        return {'position': [0,-70], 'speed': 500, 'length': 50, 'width': 1}

    def _getRaindropEndPosition(self, raindrop):
        """Use infos of a single raindrop to know the end point to be drawn on the screen"""
        start_position = raindrop['position']
        length = raindrop['length']
        rain_heading = (self._rain_heading[0]+self._wind, self._rain_heading[1])
        movementx, movementy = (rain_heading[0] * length, rain_heading[1] * length)
        return [raindrop['position'][0]+movementx, raindrop['position'][1]+movementy]

    def _generateRaindrop(self, totallyRandom=False):
        """Generate a raindrop, changing the raindrop position or generating a new one.
        Set totallyRandom parameter to False if you don't want to generate the raindrop outside the screen.
        The default value (True) is used in level init, where some raindrops can be on the screen yet. 
        """
        raindrop = self.emptyRainDrop
        raindrop['position'][0] = cbrandom.randint(0, self._surface_size[0]+50)
        if totallyRandom:
            raindrop['position'][1] = cbrandom.randint(-70, self._surface_size[1])
        else:
            raindrop['position'][1] = -70
        raindrop['speed'] = cbrandom.randint(500, 800)
        raindrop['length'] = cbrandom.randint(20, 50)
        raindrop['width'] = cbrandom.choice( (1,2) )
        return raindrop

    def draw(self, surface):
        for raindrop in self._raindrops:
            if raindrop:
                pygame.draw.line(surface,
                                 self._color,
                                 raindrop['position'],
                                 self._getRaindropEndPosition(raindrop),
                                 raindrop['width'])

    def update(self, time_passed):
        """Update the rain animation"""
        surface_size = self._surface_size
        for x in range(len(self._raindrops)):
            raindrop = self._raindrops[x]
            if not raindrop and x<self._raindrops_length:
                raindrop = self._generateRaindrop(totallyRandom=False)
                self._raindrops[x] = raindrop
            elif not raindrop:
                continue
            distance = time_passed * raindrop['speed']
            rain_heading = (self._rain_heading[0]+self._wind, self._rain_heading[1])
            movementx, movementy = (rain_heading[0] * distance, rain_heading[1] * distance)
            raindrop['position'] = [raindrop['position'][0]+movementx, raindrop['position'][1]+movementy]
            if raindrop['position'][1]+raindrop['length'] > surface_size[1]:
                self._raindrops[x] = None

        self._time_rain_frequency-= time_passed
        self._time_wind_strength-= time_passed
        if self._time_rain_frequency<=0:
            self.changeRainFrequency()
        if self._time_wind_strength<=0:
            self.changeWindStrength()

    def changeRainFrequency(self):
        self._time_rain_frequency = cbrandom.randint(20,60)
        ndrops = self._raindrops_length
        ndrops = ndrops + cbrandom.randint(-20,20)
        if ndrops<4:
            ndrops = 4
        elif ndrops>MAX_RAINDROPS:
            ndrops = MAX_RAINDROPS
        logging.info("Rain frequency changed from %s to %s" % (self._raindrops_length, ndrops))
        self._raindrops_length = ndrops

    def changeWindStrength(self):
        self._time_wind_strength = cbrandom.randint(10,20)
        wind = self._wind
        wind = cbrandom.choice( (-.4,-.3,-.2,-.1,0) )
        logging.info("Wind strength changed from %s to %s" % (self._wind, wind))        
        self._wind = wind