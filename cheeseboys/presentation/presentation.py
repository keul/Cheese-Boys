# -*- coding: utf-8 -

import logging
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

    AUTHOR(s) OF CHEESE BOYS GAME AREN'T RESPONSIBLE FOR DAMAGE YOU GET FROM A BAD PRESENTATION FILE!!!    
    """
    
    def __init__(self, level, presentation_file, presentation_dir="data/presentations"):
        self.level = level
        self.parser = PresentationParser(presentation_file, presentation_dir)
        self.parser.load()
        self.data = self.parser.data
        self._time_collected = 0
    
    def enablePresentationMode(self):
        """Disable all keys and buttons that user can press to do action in the game.
        Exception for ESC key and SPACE.
        """
        cblocals.global_controlsEnabled = False
        cblocals.globals['text_tips'] = False
        cblocals.globals['points'] = False
    
    def disablePresentationMode(self):
        """Enable all keys and buttons that user can press. Commonly called at the end of the presentation so the player can
        obtain controls back.
        """
        cblocals.global_controlsEnabled = True
        cblocals.globals['text_tips'] = True
        cblocals.globals['points'] = True

    @classmethod
    def timestampValueToString(cls, value):
        """Given a millisecond amount, format it in a timestamp format"""
        hh = mm = ss = ml = ""
        mmInHour = 1000*60*60
        mmInMinute = 1000*60
        hh = "%02d" % (value / mmInHour)
        value = value % mmInHour
        mm = "%02d" % (value / mmInMinute)
        value = value % mmInMinute
        ss = "%02d" % (value / 1000)
        ml = "%03d" % (value % 1000)
        return "%s:%s:%s %s" % (hh, mm, ss, ml)

    @classmethod
    def timestampStringToValue(cls, timestamp):
        """Given a timestamp, return the relative millisecond amount"""
        hh = int(timestamp[:2])
        mm = int(timestamp[3:5])
        ss = int(timestamp[6:8])
        ml = int(timestamp[9:12])
        return ml + ss*1000 + mm*1000*60 + hh*1000*60*60
    
    def update(self, time_passed):
        """Update presentation run timer, and run commands if needed"""
        self._time_collected+= time_passed
        try:
            next_ops = self.data['operations'][0]
        except IndexError:
            # Presentation is finished
            self.disablePresentationMode()
            return None
        next_op_timestamp_value = self.timestampStringToValue(next_ops['timestamp_start'])
        if self._time_collected*1000.>=next_op_timestamp_value:
            # I'm late, I must run next operation!
            try: 
                next_op = next_ops['commands'].pop(0)
                logging.info("Presentation: running command: %s" % next_op)
                return next_op
            except IndexError:
                # No more commands for this timestamp
                self.data['operations'].pop(0)
        return ""