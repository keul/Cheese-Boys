# -*- coding: utf-8 -

import pygame

can_attack_cursor_string = (
      "XX                      ",
      "XXX                     ",
      "XXXX                    ",
      "XXXXX                   ",
      "XXXXXX                  ",
      "XXXXXXX                 ",
      "XXXXXXXX                ",
      "XXXXXXXXX               ",
      "XXXXXXXXXX              ",
      "XXXXXXXXXXX             ",
      "XXXXXXXXXXXX            ",
      "XXXXXXXXXXXXX           ",
      "XXXXXXXXXXXXX           ",
      "XX.XXXXXXX              ",
      "XXXX XXXXXX             ",
      "XX   XXXXXX             ",
      "     XXXXXX             ",
      "      XXXXXX            ",
      "      XXXXXX            ",
      "       XXXX             ",
      "       XX               ",
      "                        ",
      "                        ",
      "                        ")


class CursorHandler(object):
    """Manage cursor change"""
    
    def __init__(self):
        self._cursor = None
    
    def changeToCombatCursor(self):
        """Change cursor to combat pointer"""
        self._cursor = pygame.cursors.compile(can_attack_cursor_string)
        pygame.mouse.set_cursor( (24,24), (1,1), *self._cursor)
    
    def changeToNormalCurson(self):
        """Change cursor to normal pointer"""
        self._cursor = pygame.cursors.compile(pygame.cursors.arrow)
        pygame.mouse.set_cursor( (24,24), (1,1), *self._cursor)

