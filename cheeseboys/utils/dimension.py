# -*- coding: utf-8 -

import pygame
from cheeseboys import cblocals


def normalizeXY(x, y):
    """Given x and y as an offset, they will be normalized at minumum of 1 pixel"""
    if x != 0 and abs(x) < 1:
        if x > 0:
            x = 1
        elif x < 0:
            x = -1
    if y != 0 and abs(y) < 1:
        if y > 0:
            y = 1
        elif y < 0:
            y = -1
    return x, y


def checkPointIsInsideRectType(point, rect):
    """Given a point and a rect, check if the point is inside this rect.
    Rect can be a pair of tuple (position, size) or a real pygame.Rect instance.
    """
    if type(rect) == tuple or type(rect) == list:
        rect = pygame.Rect(rect[0], rect[1])
    # Here rect is a pygame.Rect
    return rect.collidepoint(point)
