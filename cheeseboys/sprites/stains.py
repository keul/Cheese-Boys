# -*- coding: utf-8 -

import pygame
from pygame.locals import *
from cheeseboys.pygame_extensions import GameSprite
from cheeseboys import cblocals, utils
from cheeseboys.cbrandom import cbrandom

class DarkLargeStain(GameSprite):
    """Static dark stain"""
    
    def __init__(self, position, dimension, *containers):
        GameSprite.__init__(self, *containers)
        self.x, self.y = position
        self.rect = pygame.Rect(position, dimension)
        self.image = utils.load_image("dark-large-stain.png", "miscellaneous")
