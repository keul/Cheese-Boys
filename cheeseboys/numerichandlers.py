# -*- coding: utf-8 -*-

__author__ = "Keul - lucafbb AT gmail.com"

import re
import logging

baseStDiceFormat = r"^\d+d\d+(\+\d|\-\d)?$"
diceRe = re.compile(baseStDiceFormat)

baseStHdFormat = r"^\d(\+\d|\-\d)?$"
hdRe = re.compile(baseStHdFormat)

class DiceHandler(object):
    """Create a dice handler, to handle string format of dices in the game.
    
    This can be something like "3d6", "2d8" or other format like "6d6+5", "1d8-1"...
    """
    
    def __init__(self, value):
        self._value = value
        
        m = diceRe.match(value)
        
        if not m:
            raise ValueError('The string "%s" did not match a valid dice format' % value)
        
        numberOfDices, typeOfDice = value.split("d")
        bonus = 0
        
        if typeOfDice.find("+")>0:
            typeOfDice, bonus = typeOfDice.split("+")
            bonus = int(bonus)
        elif typeOfDice.find("-")>0:
            typeOfDice, bonus = typeOfDice.split("-")
            bonus = -int(bonus)
        
        self.numberOfDices = int(numberOfDices)
        self.typeOfDice = int(typeOfDice)
        self.bonus = bonus
        
        if self.numberOfDices<1 or self.typeOfDice<1:
            raise ValueError("Bad int values for %s" % value)
        
        logging.debug("%s --> %s %s %s" % (value, self.numberOfDices, self.typeOfDice, self.bonus))
    
    def getValues(self):
        """Return int value stored by the object handler"""
        return (self.numberOfDices, self.typeOfDice, self.bonus)

