# -*- coding: utf-8 -

import os
import os.path
import re
from cheeseboys.presentation.utils import timestamp_sort, timestampValueToString, timestampStringToValue

FIRST_LINE_REGEXP = r"""^#(\s)*version:(\s)*(\d)+\.(\d)+\.(\d)+(\s)*$"""
VERSION_NUMBERS = r"""^(\s)*(\d)+\.(\d)+\.(\d)+(\s)*$"""
re_versionLineCheck = re.compile(FIRST_LINE_REGEXP)
re_versionLine = re.compile(FIRST_LINE_REGEXP)

TIMESPAMP_LINE_ABSOLUTE_REGEXP = r"""^(\s)*(\[\d\d:\d\d:\d\d \d\d\d\])(\s)*(#.*)?$"""
re_timeStampAbsoluteCheck = re.compile(TIMESPAMP_LINE_ABSOLUTE_REGEXP)

TIMESPAMP_LINE_REGEXP = r"""^(\s)*(\[\d\d:\d\d:\d\d \d\d\d\]|\[\+\d\d:\d\d:\d\d \d\d\d])(\s)*(#.*)?$"""
re_timeStampCheck = re.compile(TIMESPAMP_LINE_REGEXP)

DATA_BLOCK_REGEXP = \
r"""
(
       \[\d\d:\d\d:\d\d[ ]\d\d\d\]
     |
       \[\+\d\d:\d\d:\d\d[ ]\d\d\d]
   )
   [ \t]*?(\#.*?)??\n                                                                   # comment after the timespamp line
(([ \t]*?.*?(\n|$))+?)
[ \t]*?(\n|$)                                                                           #    final whitespaces
"""
re_dataBlock = re.compile(DATA_BLOCK_REGEXP, re.VERBOSE)

TIMESTAMPS_DATA_REGEXP = r"""^\[(\+?\d\d:\d\d:\d\d \d\d\d)\]"""
re_timestampsData = re.compile(TIMESTAMPS_DATA_REGEXP)

class PresentationParser(object):
    """A parser for cheeseboys presentation (.cbp) files"""
    
    def __init__(self, presentation_file, presentation_dir="data/presentations"):
        self.presentation_file = presentation_file
        self.presentation_dir = presentation_dir
        self._f = self.text = None
        self.data = {}

    def load(self):
        """Open presentation file so we are ready for read.
        """
        self._f = open(os.path.join(self.presentation_dir, self.presentation_file))
        self.text = self._f.read()
        self._lines = self.text.split("\n")
        self._f.close()
        self._loadData()
    
    def _prepareDataBlock(self, data):
        """Given a data in raw format, remove white spaces and split it in a list"""
        return [x.strip() for x in data.split("\n") if x.strip()]
    
    def checkSyntax(self):
        """Parse file format and return nothing if is valid, error message otherwise"""
        # BBB: very incomplete
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

    def _replaceRelativeTimeStamps(self, operations):
        """Looking all timestamps, if a relative ones if found, it is replaced with
        the absolute value calculated on the last absolute timestamps found.
        
        Be aware that this method must be called before the sort of the data structure,
        or all [+xxx...] timestamps will be putted at the end.
        """
        collected_time = 0
        for op in operations:
            timestamp = op['timestamp']
            if timestamp.startswith("+"):
                # relative
                value = timestamp[1:]  # skip the '+' char
                collected_time += timestampStringToValue(value)
                ts = timestampValueToString(collected_time)
                op['timestamp'] = ts
            else:
                collected_time = timestampStringToValue(timestamp)

    def _loadData(self):
        """Load data from the text file to a navigable structure.
        
        data = { 'version': (x,y,z), 'operations': operations_arr }
        operations_arr = [ { 'timestamp': timestamp, 'commands' : commands_arr }, ... ]
        commands_arr = [command, ...]
        
        operations_arr list is sorted by timestamp info
        """
        if self.data:
            return self.data
        self.checkSyntax() 
        operations = []
        all_data = re_dataBlock.findall(self.text)
        for fdata in all_data:
            localData = {}
            timestamp = self._getTimeStamp(fdata[0])
            localData['timestamp'] = timestamp
            localData['commands'] = self._getCommands(self._prepareDataBlock(fdata[2]))
            operations.append(localData)
        # replace relative timestamps with absolute ones
        self._replaceRelativeTimeStamps(operations)
        # sort of the list, in case that the file isn't sorted itself
        operations.sort(timestamp_sort)
        self.data['operations'] = operations

    def _getTimeStamp(self, data):
        """Given a timestamp string return the timestamp value"""
        all_data = re_timestampsData.findall(data)
        return all_data[0]

    def _getParamsFromStr(self, paramStr):
        """Given a string with parameter semicolon-separated, return an array of params
        BBB: security issue here!
        """
        rawParams = [x.strip() for x in paramStr.split(";")]
        for x in range(len(rawParams)):
            p = rawParams[x]
            if (p.startswith("(") and p.endswith(")")) or \
               (p.startswith("[") and p.endswith("]")) or \
               p.isdigit():
                rawParams[x] = eval(p)
            elif p.startswith("\"") and p.endswith("\""):
                rawParams[x] = p[1:-1]
        return rawParams

    def _getCommands(self, data):
        """Given a list of string, obtain a commands-style list.
        Just return strings!
        """
        # The idea WAS to obtain a new language for the presentation format, but this was very
        # difficult... ok not impossible, but I've not much time for cheese boys so I need to
        # stay simple!
        #BBB: security issue here!
        return data

    @classmethod
    def replaceCbpFileAbsoluteTimestamps(cls, filename, first_timestamp=None, outFile=None):
        """
        Given a cbp valid file, replace all absolute timestamps with a relative ones,
        putting results in a new file.
        
        @filename: absolute or relative path to the .cbp file to use.
        @first_timestamp: if used, start to replace only after found this absolute timestamp (that is keeped).
        @outFile: where save the modified cbp file. If omitted a file named "newXXXX" will be created in the working directory.
        """
        try:
            pp = PresentationParser(filename, presentation_dir='')
            pp.load()
        except IOError:
            # try adding the current cwd
            pp = PresentationParser(os.path.join(os.getcwd(),filename), presentation_dir='')
            pp.load()
        
        if not outFile:
            newFname = "new-" + os.path.basename(filename)
            outFile = os.path.join(os.getcwd(),newFname)
        
        out = ""
        cnt = 0
        timevalue = None
        for line in pp.text.split("\n"):
            cnt+=1
            if not first_timestamp and re_timeStampAbsoluteCheck.match(line) and timevalue is not None:
                old_ts = re_timeStampAbsoluteCheck.findall(line)[0][1][1:13]
                old_ts_value = timestampStringToValue(old_ts)
                new_timevalue = old_ts_value-timevalue
                new_ts = "+"+timestampValueToString(new_timevalue)
                timevalue+= new_timevalue
                print "replacing at line %s: timestamp %s with %s" % (cnt, old_ts, new_ts)
                out+=line.replace(old_ts, new_ts)
            else:
                out+=line
            if (timevalue is None and re_timeStampAbsoluteCheck.match(line)) or \
               (first_timestamp and re_timeStampAbsoluteCheck.match(line)):
                # This is executed only once, or until found first_timestamp
                old_ts = re_timeStampAbsoluteCheck.findall(line)[0][1][1:13]
                print "keeping absolute timestamp at line %s: %s" % (cnt, old_ts)
                timevalue = timestampStringToValue(old_ts)
                if old_ts==first_timestamp:
                    # stop from entering there
                    first_timestamp = None
            out+="\n"

        fh = open(outFile, 'w')
        fh.write(out)
        fh.close()
        
        print "\nDone"




class CBPParsingException(Exception):
    """Exception in parsing .cbp files"""

    def __init__(self, msg, line_number=None):
        if line_number:
            lninfo_str = "line %s: " % line_number
        else:
            lninfo_str = ""
        Exception.__init__(self, "%s%s" % (lninfo_str,msg))


