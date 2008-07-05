# -*- coding: utf-8 -

import pygame

class GameSprite(pygame.sprite.Sprite):
    """Base character for game sprite. This is a normal pygame sprite with some other methods"""
    
    def __init__(self, *containers):
        pygame.sprite.Sprite.__init__(self, *containers)

    def getTip(self):
        """Print a tip text near the character.
        Override this for subclass if you wan this"""
        return ""

    def topleft(self, x=0, y=0):
        """Return top left position for this sprite"""
        if x or y:
            data = self.rect.topleft
            return data[0]+x, data[1]+y
        return self.rect.topleft