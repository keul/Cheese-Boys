# -*- coding: utf-8 -

import pygame
import locals
from gameobjects.vector2 import Vector2

def load_image(file_name, directory="", charasFormatImage=False):
    """Load an image from filesystem, from standard directory"""
    if charasFormatImage:
        return _imagesInCharasFormat(file_name, directory)
    if not directory:
        path = "%s/%s" % (locals.IMAGES_DIR_PATH, file_name)
    else:
        path = "%s/%s/%s" % (locals.IMAGES_DIR_PATH, directory, file_name)
    return pygame.image.load(path)

def _imagesInCharasFormat(file_name, directory=""):
    """Load an image from filesystem, from standard directory.
    Return an array of 12 images taken from a standard charas image.
    """
    if not directory:
        path = "%s/%s" % (locals.IMAGES_DIR_PATH, file_name)
    else:
        path = "%s/%s/%s" % (locals.IMAGES_DIR_PATH, directory, file_name)
    
    # Load the 3x4 image
    mainImage = pygame.image.load(path)
    imgXSize, imgYSize = locals.TILE_IMAGE_DIMENSION
    imgArray = []
    
    for y in range(4):
        for x in range(3):
            imgArray.append(mainImage.subsurface( (x*imgXSize,y*imgYSize), (imgXSize,imgYSize), ))
    
    return imgArray