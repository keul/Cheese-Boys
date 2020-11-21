# -*- coding: utf-8 -

import pygame
from cheeseboys import cblocals
from cheeseboys.utils.image import load_image


def changeMouseCursor(type):
    """Load a mouse cursor of the given type"""
    if type == cblocals.IMAGE_CURSOR_ATTACK_TYPE:
        cblocals.global_mouseCursor = load_image(
            cblocals.IMAGE_CURSOR_ATTACK_IMAGE, directory="mouse_pointers"
        )
        cblocals.global_mouseCursorType = type
    elif type == cblocals.IMAGE_CURSOR_CHANGELEVEL_TYPE:
        cblocals.global_mouseCursor = load_image(
            cblocals.IMAGE_CURSOR_CHANGELEVEL_IMAGE, directory="mouse_pointers"
        )
        cblocals.global_mouseCursorType = type
    elif type == cblocals.IMAGE_CURSOR_OPENDOOR_TYPE:
        cblocals.global_mouseCursor = load_image(
            cblocals.IMAGE_CURSOR_OPENDOOR_IMAGE, directory="mouse_pointers"
        )
        cblocals.global_mouseCursorType = type
    elif not type:
        cblocals.global_mouseCursor = cblocals.global_mouseCursorType = None
    else:
        raise ValueError("Cannot load cursor of type %s" % type)


def drawCursor(screen, xxx_todo_changeme):
    (x, y) = xxx_todo_changeme
    mouse_cursor = cblocals.global_mouseCursor
    x -= mouse_cursor.get_width() / 2
    y -= mouse_cursor.get_height() / 2
    screen.blit(mouse_cursor, (x, y))
