# -*- coding: utf-8 -*-

__author__ = "Keul - lucafbb AT gmail.com"
__version__ = "0.0.4"

from pygame.locals import USEREVENT

DIRECTION_N = 'N'
DIRECTION_E = 'E'
DIRECTION_S = 'S'
DIRECTION_W = 'W'
DIRECTION_NE = 'NE'
DIRECTION_SE = 'SE'
DIRECTION_SW = 'SW'
DIRECTION_NW = 'NW'

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480

TILE_IMAGE_DIMENSION = (24, 32)

MIN_PX_4_IMAGES_CHANGE = 20

DEFAULT_FONT = "Vera.ttf"

FONTS_DIR_PATH = "data/font"
IMAGES_DIR_PATH = "data/images"

DEBUG = False

# EVENTS
ATTACK_OCCURRED_EVENT = USEREVENT +1

# globals
default_font = None
global_lastMouseLeftClickPosition = ()
global_lastMouseRightClickPosition = ()

#globals = {'default_font': None}