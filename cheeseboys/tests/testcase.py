# -*- coding: utf-8 -*-

__author__ = "Keul - lucafbb AT gmail.com"

import unittest


class CheeseBoysTestCase(unittest.TestCase):
    """My own extension of the base TestCase class"""

    def setUp(self):
        """Set the random generation module to debug mode."""
        # cbrandom.toggleDebugMode(True)

    def tearDown(self):
        """Restore random generation to normal"""
        # cbrandom.toggleDebugMode()
        # cbrandom.preset_values = []

    def setDebugRandomValues(self, lst):
        """With lst, set the next fake random numbers.
        Use lst but reversed.
        """
        cbrandom.preset_values = lst
