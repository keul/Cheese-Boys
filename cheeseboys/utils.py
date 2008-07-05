# -*- coding: utf-8 -

import pygame
import cblocals

# BBB: I import this way because I'm planning to remove dependencies of WillMcGugan game-objects library.
# Better: if original vector2 class is available keep using it!
from gameobjects.vector2 import Vector2

def load_image(file_name, directory="", charasFormatImage=False, weaponInAndOut=False):
    """Load an image from filesystem, from standard directory.
    file_name will the name of the file or a tuple of 2 file name (if weaponInAndOut is used)
    charasFormatImage is used to load not a single image but an array of 12 images in charas format.
    weaponInAndOut is used to load not 12 but 24 images. The first 12 are normal images with weapon, the others are without.
    This is only used for charas that can do combat action.
    """
    if charasFormatImage:
        return _imagesInCharasFormat(file_name, directory, weaponInAndOut)
    if not directory:
        path = "%s/%s" % (cblocals.IMAGES_DIR_PATH, file_name)
    else:
        path = "%s/%s/%s" % (cblocals.IMAGES_DIR_PATH, directory, file_name)
    return pygame.image.load(path).convert_alpha()

def _imagesInCharasFormat(file_name, directory="", weaponInAndOut=False):
    """Load an image from filesystem, from standard directory.
    Return an array of 12 images taken from a standard charas image.
    The images will be 24 if weaponInAndOut is used, to get the "without weapon" series of the same charas.
    """
    if not weaponInAndOut:
        # Transform image always in a tuple, so I will act in the same way even if dont' using weaponInAndOut
        file_name = (file_name,)

    imgXSize, imgYSize = cblocals.TILE_IMAGE_DIMENSION
    imgArray = []

    for fname in file_name:
        if not directory:
            path = "%s/%s" % (cblocals.IMAGES_DIR_PATH, fname)
        else:
            path = "%s/%s/%s" % (cblocals.IMAGES_DIR_PATH, directory, fname)
    
        # Load the 3x4 image
        mainImage = pygame.image.load(path)

        for y in range(4):
            for x in range(3):
                imgArray.append(mainImage.subsurface( (x*imgXSize,y*imgYSize), (imgXSize,imgYSize), ))
    
    return imgArray

def normalizeXY(x, y):
    """Given x and y as rect offset, they will be normalized as at minumum of 1 pixel"""
    if x!=0 and abs(x)<1:
        if x>0: x=1
        elif x<0: x=-1
    if y!=0 and abs(y)<1:
        if y>0: y=1
        elif y<0: y=-1
    return x,y

# ******* CURSOR *******
def changeMouseCursor(type):
    """Load a mouse cursor of the given type"""
    if type==cblocals.IMAGE_CURSOR_ATTACK_TYPE:
        cblocals.global_mouseCursor = load_image(cblocals.IMAGE_CURSOR_ATTACK_IMAGE)
    elif not type:
        cblocals.global_mouseCursor = None
    else:
        raise ValueError("Cannot load cursor of type %s" % type)

def drawCursor(screen, (x, y) ):
    mouse_cursor = cblocals.global_mouseCursor
    x-= mouse_cursor.get_width() / 2
    y-= mouse_cursor.get_height() / 2
    screen.blit(mouse_cursor, (x,y))
# **********************