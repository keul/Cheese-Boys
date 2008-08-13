# -*- coding: utf-8 -

import pygame
from pygame.locals import *
from cheeseboys.pygame_extensions import GameSprite

class PhysicalBackground(GameSprite):
    """This is a fake sprite. Object of this class doesn't draw anything but are (commonly)
    placed where the background draw something physical (a pit, a wall, ...).
    """
    
    def __init__(self, position, dimension, *containers):
        GameSprite.__init__(self, *containers)
        self.rect = pygame.Rect(position, dimension)
        srf = pygame.Surface(dimension, flags=SRCALPHA, depth=32).convert_alpha()
        srf.set_alpha(0)
        self.image = srf