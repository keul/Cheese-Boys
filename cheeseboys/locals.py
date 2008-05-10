# -*- coding: utf-8 -*-

__version__ = "0.0.3"

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

IMAGES_DIR_PATH = "data/images"

DEBUG = False

# globals
default_font = None
screen = None
global_lastMouseLeftClickPosition = ()
global_lastMouseRightClickPosition = ()