# -*- coding: utf-8 -

import pygame
from pygame import sprite

class GameGroup(sprite.Group):
    """Game specific version of PyGame Group class, adding some functionality needed by this game.
    """
    
    def __init__(self, name, updatable=False):
        sprite.Group.__init__(self)
        self.name = name
        self._updatable = updatable
    
    @property
    def updatable(self):
        """Updatable groups stored in GameLevel object will be updated calling the update method"""
        return self._updatable
    
    # ******* DEBUG HELPER METHODS *******
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

    def drawNavPoint(self, surface, color=(255,0,0), radius=3):
        """Draw a point to the character navPoint"""
        for sprite in self.sprites():
            if hasattr(sprite,'navPoint') and sprite.navPoint:
                pos = sprite.currentLevel.transformToScreenCoordinate(sprite.navPoint.as_tuple())
                pos = (int(pos[0]), int(pos[1]))
                pygame.draw.circle(surface, color, pos, radius, 0)
    # *******

    def drawAttacks(self, surface, time_passed):
        """Given a surface, draw all attack for charas on this surface.
        Drawing an attach is done by calling charas.drawAttack.
        """
        for sprite in self.sprites():
            sprite.drawAttack(surface, time_passed)

    def rectCollisionWithCharacterHeat(self, character, rect):
        """Check if a rect is in collision with heat_rect of character of this group"""
        collisionList = []
        for sprite in self.sprites():
            if sprite is not character:
                if rect.colliderect(sprite.heat_rect):
                    collisionList.append(sprite)
        return collisionList
        