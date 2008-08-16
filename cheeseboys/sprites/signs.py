# -*- coding: utf-8 -

import pygame
from pygame.locals import *
from cheeseboys.pygame_extensions import GameSprite
from cheeseboys import cblocals, utils
from cheeseboys.cbrandom import cbrandom

class CodigoroSign(GameSprite):
    """Static town sign"""
    
    def __init__(self, position, dimension, *containers):
        GameSprite.__init__(self, *containers)
        self.rect = pygame.Rect(position, dimension)
        self.image = utils.load_image("codigoro-sign.png", "miscellaneous")

    @property
    def collide_rect(self):
        """See GameSprite.collide_rect.
        The sign collide rect is the little basement area.
        """
        rect = self.rect
        ly = rect.bottom
        h = 5
        hy = ly-h
        lx = rect.left + 33
        w = 9
        return pygame.Rect( (lx, hy), (w, h) )