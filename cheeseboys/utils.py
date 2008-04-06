# -*- coding: utf-8 -

import pygame

def load_image(file_name):
    """Load an image from filesystem, from standard directory"""
    return pygame.image.load("data/images/%s" % file_name)