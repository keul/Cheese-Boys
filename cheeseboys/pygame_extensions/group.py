# -*- coding: utf-8 -

import pygame
from pygame import sprite

from cheeseboys import utils

class GameGroup(sprite.Group):
    """Game specific version of PyGame Group class, adding some functionality needed by this game.
    """
    
    def __init__(self, name, drawable=False, updatable=False):
        sprite.Group.__init__(self)
        self.name = name
        self._updatable = updatable
        self._drawable = drawable

    def sprites(self):
        """Return a list of all sprites in this group.
        This method is overloaded from the standard pygame.Group class because the engine need
        to obtain sprites ordered by the sprite y-axis.
        This way, drawing the sprite in the order obtained, we get the draw correct as soon as
        a sprite is "far" from the screen base.
        """
        sprites = sprite.Group.sprites(self)
        sprites.sort(utils.groupSortingByYAxis)
        return sprites
   
    @property
    def updatable(self):
        """Updatable groups stored in GameLevel object will be updated calling the update method"""
        return self._updatable

    @property
    def drawable(self):
        """Drawable groups stored in GameLevel object will be draw on screen"""
        return self._drawable

    def drawAttacks(self, surface, time_passed):
        """Given a surface, draw all attack for charas on this surface.
        Drawing an attach is done by calling charas.drawAttack.
        
        Of course, this method is nonsense called on a group that store non-character GameSprite.
        """
        for character in self.sprites():
            character.drawAttack(surface, time_passed)

    def rectCollisionWithCharacterHeat(self, character, rect):
        """Check if a rect is in collision with heat_rect of character of this group"""
        collisionList = []
        for sprite in self.sprites():
            if sprite is not character:
                if rect.colliderect(sprite.heat_rect):
                    collisionList.append(sprite)
        return collisionList




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