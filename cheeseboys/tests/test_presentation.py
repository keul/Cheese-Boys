# -*- coding: utf-8 -*-

__author__ = "Keul - lucafbb AT gmail.com"

import unittest
from testcase import CheeseBoysTestCase
from cheeseboys.presentation import Presentation
from cheeseboys.presentation.presentation_parser import PresentationParser, CBPParsingException

FAKE_CBP_FILE = \
"""


       #    version: 1.0.0

[00:00:00 000]
    level.topleft: (100,100)
    abc

[00:00:02 000 - 00:00:05 000]
    level.normalizeDrawPositionBasedOn: (100,700)
    ddd
"""

class TestPresentationParser(CheeseBoysTestCase):
    """Test the use of a PresentationParser"""
    
    def setUp(self):
        CheeseBoysTestCase.setUp(self)
        self.pparser = PresentationParser("dummy")
        # init parameter, as I will never call .open()
        self.pparser._text = FAKE_CBP_FILE
        self.pparser._lines = self.pparser._text.split("\n")
    
    def testVersionLine(self):
        """Test if version line is found and parsed right"""
        line = self.pparser._lines[5]
        self.assertRaises(CBPParsingException, self.pparser._checkVersionLineSyntax, line, 6)
        line = self.pparser._lines[3]
        self.assertRaises(CBPParsingException, self.pparser._checkVersionLineSyntax, line, 4)
        self.assertRaises(CBPParsingException, self.pparser._checkVersionLineSyntax, line.strip()+ "   # no comment on version line", 4)
        self.assertEquals(self.pparser._checkVersionLineSyntax(line.strip(), 4), (1,0,0))

    def testCheckSyntax(self):
        """Check that application can handle correctly a whole file block"""
        self.assertEquals(self.pparser.checkSyntax(), None)

    def test_loadTimeStampsStartEnd(self):
        """Check loading for timestamps value(s)"""
        self.assertEquals(self.pparser._getTimeStampsStartEnd("[00:00:00 000]"), ("00:00:00 000", None))
        self.assertEquals(self.pparser._getTimeStampsStartEnd("[00:00:00 001 - 00:01:00 999]"), ("00:00:00 001", "00:01:00 999"))        

    def test_loadData(self):
        """Test the loading of a complete commands datablock"""
        self.pparser._loadData()
        self.assertEquals(self.pparser.data['operations'][1]['commands'][0], "level.normalizeDrawPositionBasedOn: (100,700)")

suites = []

suites.append(unittest.TestLoader().loadTestsFromTestCase(TestPresentationParser))

alltests = unittest.TestSuite(suites)