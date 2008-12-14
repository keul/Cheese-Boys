# -*- coding: utf-8 -

import pygame
from cheeseboys.pygame_extensions import GameSprite
from cheeseboys import cblocals

class Trigger(GameSprite):
    """Triggers are invisible sprites used to raise events in the game when other GameSprite
    objects run over the area of the trigger itself (AKA fire the trigger).
    
    Normally a trigger disable itself when it's fired, but you can change this setting the Trigger.disableTriggerAfterFire
    attribute to False.
    
    You must also specify the fireOnCollistionWith collection of groups and/or sprites that fire the trigger.
    
    External code can use the setOptions method to pass some data to the trigger subtype in a common way
    (implemented only in subclasses).
    
    When a trigger is fired, a TRIGGER_FIRED_EVENT is raised. This event is used for retrieve some info from the trigger
    itself, by using the Trigger.getResult method (implemented in subclasses).
    """
    
    def __init__(self, position, size, fireOnCollistionWith=(), *containers):
        GameSprite.__init__(self, *containers)
        self.rect = pygame.Rect(position, size)
        self.position = position
        srf = self.generateEmptySprite(size, alpha=0)
        if cblocals.DEBUG:
            srf.set_alpha(100)
            srf.fill( (255,255,255) )
        self.image = srf
        # Other important trigger's members
        self.disableTriggerAfterFire = True
        self.fireOnCollistionWith = fireOnCollistionWith

    def update(self, time_passed):
        """Check if something is touching the trigger, and if the trigger must be fired.
        """
        GameSprite.update(self, time_passed)
        collide_rect = self.collide_rect
        for member in self.fireOnCollistionWith:
            if member is self:
                continue
            if hasattr(member, 'sprites'):
                # is a group
                for sprite in member.sprites():
                    if sprite.collide_rect.colliderect(collide_rect):
                        self.fireTrigger(sprite)
                        return
            else:
                # is a sprite
                if member.collide_rect.colliderect(collide_rect):
                    self.fireTrigger(member)
                    return

    def fireTrigger(self, sprite):
        """Called when the trigger gets fired. The sprite param is the sprite that start the action"""
        event = pygame.event.Event(cblocals.TRIGGER_FIRED_EVENT, {'trigger': self, 'sprite': sprite})
        pygame.event.post(event)
        if self.disableTriggerAfterFire:
            self.kill()

    def setOptions(self, **kwargs):
        """Used in subclasses to get some data for the trigger type and the actions to do.
        This must be implemented in subclasses.
        """
        raise NotImplementedError("The setOptions method is not implemented in the Trigger class")

    def getResult(self):
        """Return some code to execute as trigger result.
        This must be implemented in subclasses.
        """
        raise NotImplementedError("The getResult method is not implemented in the Trigger class")
