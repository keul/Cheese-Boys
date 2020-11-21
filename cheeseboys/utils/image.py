# -*- coding: utf-8 -

import pygame
from pygame.locals import *
from cheeseboys import cblocals
from cheeseboys.cbrandom import cbrandom


def load_image(
    file_name,
    directory="",
    charasFormatImage=False,
    weaponInAndOut=False,
    simpleLoad=False,
):
    """Load an image from filesystem, from standard directory.
    @file_name: the file image name, or a tuple of 2 file name (if weaponInAndOut is used).
    @directory: the subdirectory from witch take the image, default to the root.
    @charasFormatImage: used to load not a single image but an array of 12 images in charas format.
    @weaponInAndOut: used to load not 12 but 24 images. The first 12 are normal images with weapon, the others are without.
    """
    if charasFormatImage:
        return _imagesInCharasFormat(file_name, directory, weaponInAndOut)
    if not directory:
        path = "%s/%s" % (cblocals.IMAGES_DIR_PATH, file_name)
    else:
        path = "%s/%s/%s" % (cblocals.IMAGES_DIR_PATH, directory, file_name)
    if simpleLoad:
        return pygame.image.load(path).convert(32, HWSURFACE | SRCALPHA)
    return pygame.image.load(path).convert_alpha()


def _imagesInCharasFormat(file_name, directory="", weaponInAndOut=False):
    """Load an image from filesystem, from standard directory.
    Return an array of 12 images taken from a standard charas image.
    The images will be 24 if weaponInAndOut is used, to get the "without weapon" series of the same charas.
    """
    if not weaponInAndOut:
        # Transform image always in a tuple, so I will act in the same way even if dont' using weaponInAndOut
        file_name = (file_name,)

    imgXSize, imgYSize = cblocals.TILE_IMAGE_SIZE
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
                imgArray.append(
                    mainImage.subsurface(
                        (x * imgXSize, y * imgYSize),
                        (imgXSize, imgYSize),
                    )
                )

    return imgArray


def getRandomImageFacingUp(images):
    """Given an image dictionary (commonly the character.images structure data) return a random image.
    This image will be rotated randomly 90 degree left or right.
    This is used to draw dead charas.
    """
    image = cbrandom.choice(list(images.values()))
    l_or_r = cbrandom.randint(1, 2)
    if l_or_r == 1:
        return pygame.transform.rotate(image, -90)
    return pygame.transform.rotate(image, 90)
