# -*- coding: utf-8 -

class Presentation(object):
    """Presentation object is a parser for special text files format that can perform
    animation of character and other sprite that commonly are moved in game action.
    
    The game creator must only write one of those .cbp (cheeseboys presentation) file in the right
    format, and the Presentation object will move the actors.
    
    Of course, Presentation are played on a real GameLevel instance.
    """
    
    def __init__(self, level, presentation_file, presentation_dir="data/presentations"):
        self.level = level
        self.presentation_file = file
        self.presentation_dir=presentation_dir