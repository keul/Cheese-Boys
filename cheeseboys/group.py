# -*- coding: utf-8 -

import pygame
from pygame import sprite

class Group(sprite.Group):
    """Custom version of PyGame Group class, adding some functionality needed by this game.
    Sprite in this class must have the collide_rect attribute.
    """
    
    def drawCollideRect(self, surface, color=(0,255,255), width=1):
        """Draw a rect on the screen that repr collide area for all Sprite in this group"""
        for sprite in self.sprites():
            pygame.draw.rect(surface, color, sprite.collide_rect, width)
    
    def drawMainRect(self, surface, color=(255,100,100), width=1):
        """Draw a rect on the screen that repr rect attribute of the sprite, for all Sprite in this group"""
        for sprite in self.sprites():
            pygame.draw.rect(surface, color, sprite.rect, width)