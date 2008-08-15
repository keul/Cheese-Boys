# -*- coding: utf-8 -

import pygame
from cheeseboys.pygame_extensions import GameSprite
from cheeseboys import cblocals

class PhysicalBackground(GameSprite):
    """This is a fake sprite. Object of this class doesn't draw anything but are (commonly)
    placed where the background draw something physical (a pit, a wall, ...).
    
    Physical background sprites holds a fake image property, that is a transparent pygame Sprite of the given
    dimension.
    """
    
    def __init__(self, position, dimension, *containers):
        GameSprite.__init__(self, *containers)
        self.rect = pygame.Rect(position, dimension)
        srf = self._loadEmptySprite(dimension)        
        if cblocals.DEBUG:
            srf.set_alpha(150)
        self.image = srf