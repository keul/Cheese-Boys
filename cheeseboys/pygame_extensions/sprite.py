# -*- coding: utf-8 -

import pygame

class GameSprite(pygame.sprite.Sprite):
    """Base character for game sprite. This is a normal pygame sprite with some other methods.
    A GameSprite is always used inside a Level object.
    """
    
    def __init__(self, *containers):
        pygame.sprite.Sprite.__init__(self, *containers)
        self.currentLevel = None

    def getTip(self):
        """Print a tip text near the character.
        Override this for subclass if you wan this"""
        return ""

    def topleft(self, x=0, y=0):
        """Return top left position for this sprite"""
        topleft = self.rect.topleft
        if x or y:
            return (topleft[0]+x, topleft[1]+y)
        return topleft