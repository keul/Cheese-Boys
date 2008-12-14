# -*- coding: utf-8 -

import pygame
from cheeseboys.pygame_extensions import GameSprite
from cheeseboys import cblocals

class PhysicalBackground(GameSprite):
    """This is a fake sprite. Object of this class doesn't draw anything but are (commonly)
    placed where the background draw something physical (a pit, a wall, ...).
    
    Physical background sprites holds a fake image property, that is a transparent pygame Sprite of the given
    size.
    """
    
    def __init__(self, position, size, *containers):
        GameSprite.__init__(self, *containers)
        self.rect = pygame.Rect(position, size)
        srf = self.generateEmptySprite(size, alpha=0)
        if cblocals.DEBUG:
            srf.set_alpha(150)
        self.image = srf