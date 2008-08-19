# -*- coding: utf-8 -*-

__author__ = "Keul - lucafbb AT gmail.com"
__version__ = "0.1.0"

from pygame.locals import USEREVENT

DIRECTION_N = 'N'
DIRECTION_E = 'E'
DIRECTION_S = 'S'
DIRECTION_W = 'W'
DIRECTION_NE = 'NE'
DIRECTION_SE = 'SE'
DIRECTION_SW = 'SW'
DIRECTION_NW = 'NW'

SCREEN_SIZE = (800, 600)
GAME_SCREEN_SIZE = (650, 600)
CONSOLE_SCREEN_SIZE = (150, 600)


TILE_IMAGE_DIMENSION = (24, 32)

MIN_PX_4_IMAGES_CHANGE = 20
HIT_MOVEMENT_SPEED = 500

DEFAULT_FONT = "Vera.ttf"

FONTS_DIR_PATH = "data/font"
IMAGES_DIR_PATH = "data/images"

IMAGE_CURSOR_ATTACK_TYPE = "ATTACK"
IMAGE_CURSOR_ATTACK_IMAGE = "icon_swords.gif"

DEBUG = False

# EVENTS
ATTACK_OCCURRED_EVENT = USEREVENT +1
SHOUT_EVENT = USEREVENT +2


# TH0
TH0_MISS = "miss"
TH0_HIT = "hit"
TH0_MISS_CRITICAL = "miss (critical)"
TH0_HIT_CRITICAL = "critical hit"


# globals
default_font = default_font_big = speech_font = None
global_lastMouseLeftClickPosition = ()
global_lastMouseRightClickPosition = ()
global_leftButtonIsDown = False
global_mouseCursor = None
gameLanguage = "en"

#globals = {'default_font': None}