# -*- coding: utf-8 -

from cheeseboys.level import loadLevelByName
from presentation_parser import PresentationParser

class Presentation(object):
    """Presentation object is a parser for special text files format that can perform
    animation of character and other sprite that commonly are moved in game action.
    
    The game creator must only write one of those .cbp (cheeseboys presentation) file in the right
    format, and the Presentation object will move the actors on the scene.
    
    Of course, Presentation are played on a real GameLevel instance.
    """
    
    def __init__(self, level, presentation_file, presentation_dir="data/presentations"):
        if type(level)==str:
            level = loadLevelByName(level)
        self.level = level
        self.parser = PresentationParser(presentation_file, presentation_dir)
        self.parser.load()
        self.data = self.parser.data

    def run(self):
        """Run the presentation this object store"""
        print self.data