# -*- coding: utf-8 -

import re

FIRST_LINE_REGEXP = r"""^#(\s)*version(\s)*(\d)+\.(\d)+\.(\d)+(\s)*(#.*)?$"""

class PresentationParser(object):
    """A parser for cheeseboys presentation (.cbp) files"""
    
    def __init__(self, presentation_file, presentation_dir="data/presentations"):
        self.presentation_file = presentation_file
        self.presentation_dir = presentation_dir
        self._f = self._text = None

    def load(self):
        """Open presentation file so we are ready for read.
        This is called automatically in object creation, but you can call
        this again to read the file from begin.
        """
        self._f = open(self.presentation_dir+"/"+self.presentation_file)
        self._text = self._f.read()
        self._lines = self._text.split("\n")
        self.close()
        self._f.close()
        
    def checkSyntax(self):
        """Parse file format and return nothing if is valid, error messages otherwise"""
        lnumber = 0
        errs = []
        checks = {'first': True}
        for line in self._lines:
            line = line.trim()
            lnumber+=1
            if not line: continue
            if line.startswith("#"):
                if checks['first']:
                    self._checkVersionLineSyntax(line)
                else:
                    continue
    
    def _checkVersionLineSyntax(self, line):
        """Check this line format"""