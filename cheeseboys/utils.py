# -*- coding: utf-8 -

import pygame
import locals

# BBB: I import this way because I'm planning to remove dependencies of WillMcGugan game-objects library.
# Better: if original vector2 is available the use it!
from gameobjects.vector2 import Vector2

def load_image(file_name, directory="", charasFormatImage=False, weaponInAndOut=False):
    """Load an image from filesystem, from standard directory.
    file_name will the name of the file or a tuple of 2 file name (if weaponInAndOut is used)
    charasFormatImage is used to load not a single image but an array of 12 images in charas format.
    weaponInAndOut is used to load not 12 but 24 images. The first 12 are normal images with weapon, the others are without.
    This is only used for charas that combat.
    """
    if charasFormatImage:
        return _imagesInCharasFormat(file_name, directory, weaponInAndOut)
    if not directory:
        path = "%s/%s" % (locals.IMAGES_DIR_PATH, file_name)
    else:
        path = "%s/%s/%s" % (locals.IMAGES_DIR_PATH, directory, file_name)
    return pygame.image.load(path)

def _imagesInCharasFormat(file_name, directory="", weaponInAndOut=False):
    """Load an image from filesystem, from standard directory.
    Return an array of 12 images taken from a standard charas image.
    The images will be 24 if weaponInAndOut is used, to get the "without weapon" series of the same charas.
    """
    if not weaponInAndOut:
        # Transform image always in a tuple, so I will act in the same way even if dont' using weaponInAndOut
        file_name = (file_name,)

    imgXSize, imgYSize = locals.TILE_IMAGE_DIMENSION
    imgArray = []

    for fname in file_name:
        if not directory:
            path = "%s/%s" % (locals.IMAGES_DIR_PATH, fname)
        else:
            path = "%s/%s/%s" % (locals.IMAGES_DIR_PATH, directory, fname)
    
        # Load the 3x4 image
        mainImage = pygame.image.load(path)
    
        
        for y in range(4):
            for x in range(3):
                imgArray.append(mainImage.subsurface( (x*imgXSize,y*imgYSize), (imgXSize,imgYSize), ))
    
    return imgArray