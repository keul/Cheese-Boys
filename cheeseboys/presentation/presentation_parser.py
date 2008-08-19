# -*- coding: utf-8 -

import re

class PresentationParser(object):
    """A parser for cheeseboys presentation (.cbp) files"""
    
    def __init__(self, presentation_file, presentation_dir="data/presentations"):
        self.presentation_file = presentation_file
        self.presentation_dir = presentation_dir
        self._f = None
        self.open()
    
    def open(self):
        """Open presentation file so we are ready for read.
        This is called automatically from object instantiation.
        """
        self._f = open(self.presentation_dir+"/"+self.presentation_file)
        
    def close(self):
        """Close opened file"""
        self._f.close()
        self._f = None
    
    def isOpen(self):
        return self._f is not None