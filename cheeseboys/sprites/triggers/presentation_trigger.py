# -*- coding: utf-8 -

import pygame
from cheeseboys.sprites.triggers import Trigger
from cheeseboys import cblocals

class PresentationTrigger(Trigger):
    """A trigger that run a presentation on the current level.
    """
    
    def __init__(self, position, dimension, fireOnCollistionWith=(), *containers):
        Trigger.__init__(self, position, dimension, fireOnCollistionWith, *containers)
        self._presentation_to_run = None
        self._presentation_dir = None

    def setOptions(self, presentation, presentation_dir):
        """Load a presentation object"""
        self._presentation_to_run = presentation
        self._presentation_dir = presentation_dir
    
    def getResult(self):
        """Run the presentation in the level"""
        return self.currentLevel.enablePresentation(self._presentation_to_run, self._presentation_dir)