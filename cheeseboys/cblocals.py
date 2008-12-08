# -*- coding: utf-8 -*-

__author__ = "Keul - lucafbb AT gmail.com"
__version__ = "0.1.1"

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
FULLSCREEN = False

TILE_IMAGE_SIZE = (24, 32)

MIN_PX_4_IMAGES_CHANGE = 20
HIT_MOVEMENT_SPEED = 500

DEFAULT_FONT = "Vera.ttf"
DEFAULT_LEVELTEXT_FONT = "Vera.ttf"
MAIN_TITLE_FONT = "Achafexp.ttf"
FONTS_DIR_PATH = "data/font"


IMAGES_DIR_PATH = "data/images"

IMAGE_CURSOR_ATTACK_TYPE = "ATTACK"
IMAGE_CURSOR_ATTACK_IMAGE = "icon_swords.gif"
IMAGE_CURSOR_CHANGELEVEL_TYPE = "CHANGELEVEL"
IMAGE_CURSOR_CHANGELEVEL_IMAGE = "poi_arrow_orange.gif"
IMAGE_CURSOR_OPENDOOR_TYPE = "OPEN"
IMAGE_CURSOR_OPENDOOR_IMAGE = "door.gif"

# ******* EVENTS *******
ATTACK_OCCURRED_EVENT = USEREVENT +1
SHOUT_EVENT = USEREVENT +2
LEVEL_CHANGE_EVENT = USEREVENT +3
SPRITE_COLLISION_EVENT = USEREVENT +4
TRIGGER_FIRED_EVENT = USEREVENT +5


# TH0
TH0_MISS = "miss"
TH0_HIT = "hit"
TH0_MISS_CRITICAL = "miss (critical)"
TH0_HIT_CRITICAL = "critical hit"

# LEVEL TEXT
LEVEL_TEXT_TYPE_BLACKSCREEN = 'blackscreen'
LEVEL_TEXT_TYPE_NORMAL = 'normal'

URL_CHEESEBOYS_LAST_VERSION = "http://keul.it/develop/python/cheeseboys/version.xml"

# globals
default_font = default_font_big = speech_font = leveltext_font = main_title_font = None
game_speed = 1.
screen = None
global_lastMouseLeftClickPosition = ()
global_lastMouseRightClickPosition = ()
global_leftButtonIsDown = False
global_mouseCursor = None
global_mouseCursorType = None
global_controlsEnabled = True
gameLanguage = "en"

# Menu
game_menu = None

globals = {'text_tips': True,
           'points': True,
           }

DEBUG = False