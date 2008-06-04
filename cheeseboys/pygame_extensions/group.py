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
    
    def drawPhysicalRect(self, surface, color=(200,200,200), width=1):
        """Draw a rect on the screen that repr real physucal rect attribute of the sprite, for all Sprite in this group"""
        for sprite in self.sprites():
            pygame.draw.rect(surface, color, sprite.physical_rect, width)

    def drawHeatRect(self, surface, color=(255,0,255), width=1):
        """Draw a rect on the screen that repr the heat area for all Sprite in this group"""
        for sprite in self.sprites():
            pygame.draw.rect(surface, color, sprite.heat_rect, width)

    def drawAttacks(self, surface, time_passed):
        """Given a surface, draw all attack for charas on this surface.
        Drawing an attach is done by calling charas.drawAttack.
        """
        for sprite in self.sprites():
            sprite.drawAttack(surface, time_passed)

    def rectCollisionWithCharacterHeat(self, character, rect):
        """Check if a rect is in collision with heat_rect of character"""
        collisionList = []
        for sprite in self.sprites():
            if sprite is not character:
                if rect.colliderect(sprite.heat_rect):
                    collisionList.append(sprite)
        return collisionList
        