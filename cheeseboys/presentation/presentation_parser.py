# -*- coding: utf-8 -

import re

FIRST_LINE_REGEXP = r"""^#(\s)*version:(\s)*(\d)+\.(\d)+\.(\d)+(\s)*$"""
VERSION_NUMBERS = r"""^(\s)*(\d)+\.(\d)+\.(\d)+(\s)*$"""

TIMESPAMP_LINE_REGEXP = r"""^(\s)*(\[\d\d:\d\d:\d\d \d\d\d\]|\[\d\d:\d\d:\d\d \d\d\d - \d\d:\d\d:\d\d \d\d\d\])(\s)*(#.*)?$"""


re_versionLineCheck = re.compile(FIRST_LINE_REGEXP)
re_versionLine = re.compile(FIRST_LINE_REGEXP)

class PresentationParser(object):
    """A parser for cheeseboys presentation (.cbp) files"""
    
    def __init__(self, presentation_file, presentation_dir="data/presentations"):
        self.presentation_file = presentation_file
        self.presentation_dir = presentation_dir
        self._f = self._text = None
        self.data = {}

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
            line = line.strip()
            lnumber+=1
            if not line: continue
            if line.startswith("#"):
                if checks['first']:
                    self._checkVersionLineSyntax(line, lnumber)
                    checks['first'] = False
                else:
                    continue # ignore comments
    
        
    
    def _checkVersionLineSyntax(self, line, lnumber):
        """Check that line format is protocol version comment"""
        if not re_versionLineCheck.match(line):
            raise CBPParsingException("First data line isn't version information; found \"%s\"" % line, lnumber)
        match_obj = re_versionLine.match(line)
        all_groups = match_obj.groups()
        self.data['version'] = (int(all_groups[2]),int(all_groups[3]),int(all_groups[4]))
        return self.data['version']

class CBPParsingException(Exception):
    """Exception in parsing .cbp files"""

    def __init__(self, msg, line_number):
        Exception.__init__(self, "line %s: %s" % (line_number,msg))


