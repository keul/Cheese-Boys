# -*- coding: utf-8 -

import pygame
from pygame.locals import *
from cheeseboys.pygame_extensions.sprite import GameSprite
from cheeseboys import cblocals, utils

class Crate(GameSprite):
    """A wood crate sprite"""
    
    def __init__(self, position, type, orientation, *containers):
        """Init the crate. You need specify the type of the crate, that will change the used image, and also the
        orientation (image can be rotated).
        @type: a integer number to be appended to the createXX.png filename.
        @orientation: an integer from 0 to 3, that rotate the image 90*value degree counterclockwise.
        """
        GameSprite.__init__(self, *containers)
        image = utils.load_image("crate%s.png" % type, directory="miscellaneous")
        if orientation:
            image = pygame.transform.rotate(image, 90*orientation)
        self.image = image
        self.position = position
        self.rect = pygame.Rect(position, image.get_size())
        self.rect.midbottom = position



