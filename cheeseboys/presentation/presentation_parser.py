# -*- coding: utf-8 -

import re

FIRST_LINE_REGEXP = r"""^#(\s)*version:(\s)*(\d)+\.(\d)+\.(\d)+(\s)*$"""
VERSION_NUMBERS = r"""^(\s)*(\d)+\.(\d)+\.(\d)+(\s)*$"""
re_versionLineCheck = re.compile(FIRST_LINE_REGEXP)
re_versionLine = re.compile(FIRST_LINE_REGEXP)

TIMESPAMP_LINE_REGEXP = r"""^(\s)*(\[\d\d:\d\d:\d\d \d\d\d\]|\[\d\d:\d\d:\d\d \d\d\d - \d\d:\d\d:\d\d \d\d\d\])(\s)*(#.*)?$"""
re_timeStampCheck = re.compile(TIMESPAMP_LINE_REGEXP)

DATA_BLOCK_REGEXP = \
r"""
(
       \[\d\d:\d\d:\d\d[ ]\d\d\d\]
     |
       \[\d\d:\d\d:\d\d[ ]\d\d\d[ ]-[ ]\d\d:\d\d:\d\d[ ]\d\d\d\]
   )
   [ \t]*?(\#.*?)??[\n]                                                                   # comment after the timespamp line
(([ \t]*?.*?[\n])+?)$
"""
re_dataBlock = re.compile(DATA_BLOCK_REGEXP, re.MULTILINE|re.VERBOSE)

TIMESTAMPS_DATA_REGEXP = r"""^\[(\d\d:\d\d:\d\d \d\d\d)\]|\[(\d\d:\d\d:\d\d \d\d\d - \d\d:\d\d:\d\d \d\d\d)\]"""
re_timestampsData = re.compile(TIMESTAMPS_DATA_REGEXP)

class PresentationParser(object):
    """A parser for cheeseboys presentation (.cbp) files"""
    
    def __init__(self, presentation_file, presentation_dir="data/presentations"):
        self.presentation_file = presentation_file
        self.presentation_dir = presentation_dir
        self._f = self._text = None
        self.data = {}

    def load(self):
        """Open presentation file so we are ready for read.
        """
        self._f = open(self.presentation_dir+"/"+self.presentation_file)
        self._text = self._f.read()
        self._lines = self._text.split("\n")
        self.close()
        self._f.close()
    
    def _prepareDataBlock(self, data):
        """Given a data in raw format, remove white spaces and split it in a list"""
        return [x.strip() for x in data.split("\n") if x.strip()]
    
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
                break
    
    def _checkVersionLineSyntax(self, line, lnumber):
        """Check that line format is protocol version comment"""
        if not re_versionLineCheck.match(line):
            raise CBPParsingException("First data line isn't version information; found \"%s\"" % line, lnumber)
        match_obj = re_versionLine.match(line)
        all_groups = match_obj.groups()
        self.data['version'] = (int(all_groups[2]),int(all_groups[3]),int(all_groups[4]))
        return self.data['version']

    def _loadData(self):
        """Load data from the text file to a navigable structure.
        data = { 'version': (x,y,z), 'operations': operations_arr }
        operations_arr = [ { 'timestamp_start': timestamp, 'timestamp_end': timestamp, 'commands' : commands_arr }, ... ]
        commands_arr = [command1, command2, ...]
        """
        if self.data:
            return self.data
        self.checkSyntax() 
        operations = []
        all_data = re_dataBlock.findall(self._text)
        for fdata in all_data:
            localData = {}
            timestamps1, timestamps2 = self._getTimeStampsStartEnd(fdata[0])
            localData['timestamp_start'] = timestamps1
            if timestamps2:
                localData['timestamp_end'] = timestamps2
            localData['commands'] = self._getCommands(self._prepareDataBlock(fdata[2]))
            operations.append(localData)
        self.data['operations'] = operations    

    def _getTimeStampsStartEnd(self, data):
        """Given a timestamps string return (timestamp1, timestamp2) or (timestamp1, None) tuples"""
        all_data = re_timestampsData.findall(data)
        for gps in all_data:
            if not gps[1]:
                return gps[0], None
            return tuple(gps[1].split(" - "))

    def _getCommands(self, data):
        """Given a list of string, obtain a commands-style list.
        BBB: for now is the list itself!
        """
        return data

    def run(self):
        """Run the presentation this object store"""
        if not self.data:
            self._loadData()

class CBPParsingException(Exception):
    """Exception in parsing .cbp files"""

    def __init__(self, msg, line_number=None):
        if line_number:
            lninfo_str = "line %s: " % line_number
        else:
            lninfo_str = ""
        Exception.__init__(self, "%s%s" % (lninfo_str,msg))


