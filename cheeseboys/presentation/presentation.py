# -*- coding: utf-8 -

from presentation_parser import PresentationParser
from cheeseboys import cblocals

class Presentation(object):
    """Presentation object is a container for special automatic operations performing
    animation of characters and other sprites that commonly are moved in game action.
    
    The game creator must only write one of those .cbp (cheeseboys presentation) file in the right
    format, and the Presentation object will move the actors on the scene.

    Of course, Presentation are played on a real GameLevel instance.
    
    NBB: the .cbp file format is (for now, but maybe it will never change) a simple list of python commands
    using Cheese Boys APIs.
    This will lead to security issues! If you write a python command that will erase your HD in a .cbp file
    this will be executed by the game!

    AUTHOR ISN'T RESPONSIBLE FOR DAMAGE YOU GET FROM A BAD PRESENTATION FILE!!!    
    """
    
    def __init__(self, level, presentation_file, presentation_dir="data/presentations"):
        self.level = level
        self.parser = PresentationParser(presentation_file, presentation_dir)
        self.parser.load()
        self.data = self.parser.data

    def getData(self):
        """get the presentation this object store"""
        return self.data
    
    def enablePresentationMode(self):
        """Disable all keys and button that user can press.
        Exception for ESC key and SPACE.
        """
        cblocals.global_controlsEnabled = False
    
    def disablePresentationMode(self):
        """Enable all keys and button that user can press, commonly called at the end of the presentation.
        """
        cblocals.global_controlsEnabled = True  