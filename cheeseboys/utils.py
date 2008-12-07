# -*- coding: utf-8 -

import pygame
import cblocals
from cheeseboys.cbrandom import cbrandom

from cheeseboys.vector2 import Vector2

def load_image(file_name, directory="", charasFormatImage=False, weaponInAndOut=False, simpleLoad=False):
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
    if simpleLoad:
        return pygame.image.load(path)
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
                imgArray.append(mainImage.subsurface( (x*imgXSize,y*imgYSize), (imgXSize,imgYSize), ))
    
    return imgArray

def normalizeXY(x, y):
    """Given x and y as an offset, they will be normalized at minumum of 1 pixel"""
#    if -0.001<x<0.001:
#        x=0
#    if -0.001<y<0.001:
#        y=0
    if x!=0 and abs(x)<1:
        if x>0: x=1
        elif x<0: x=-1
    if y!=0 and abs(y)<1:
        if y>0: y=1
        elif y<0: y=-1
    return x,y

def getRandomImageFacingUp(images):
    """Given an image dictionary (commonly the character.images structure data) return a random image.
    This image will be rotated randomly 90 degree left or right.
    This is used to draw dead charas.
    """
    image = cbrandom.choice(images.values())
    l_or_r = cbrandom.randint(1,2)
    if l_or_r==1:
        return pygame.transform.rotate(image, -90)
    return pygame.transform.rotate(image, 90)

def checkPointIsInsideRectType(point, rect):
    """Given a point and a rect, check if the point is inside this rect.
    Rect can be a pair of tuple (position, size) or a real pygame.Rect instance.
    """
    if type(rect)==tuple or type(rect)==list:
        rect = pygame.Rect( rect[0], rect[1] )
    # Here rect is a pygame.Rect
    return rect.collidepoint(point)

def groupSortingByYAxis(sprite1, sprite2):
    """This function is made to be used by the sort procedure of the GameGroup.sprites().
    Order 2 sprites by their Y position (using the GameSprite.collide_rect.centery)
    """
    y1 = sprite1.collide_rect.centery
    y2 = sprite2.collide_rect.centery
    if y1>y2:
        return 1
    elif y1==y2:
        return 0
    return -1

# ******* CURSOR *******
def changeMouseCursor(type):
    """Load a mouse cursor of the given type"""
    if type==cblocals.IMAGE_CURSOR_ATTACK_TYPE:
        cblocals.global_mouseCursor = load_image(cblocals.IMAGE_CURSOR_ATTACK_IMAGE, directory="mouse_pointers")
        cblocals.global_mouseCursorType = type
    elif type==cblocals.IMAGE_CURSOR_CHANGELEVEL_TYPE:
        cblocals.global_mouseCursor = load_image(cblocals.IMAGE_CURSOR_CHANGELEVEL_IMAGE, directory="mouse_pointers")
        cblocals.global_mouseCursorType = type
    elif type==cblocals.IMAGE_CURSOR_OPENDOOR_TYPE:
        cblocals.global_mouseCursor = load_image(cblocals.IMAGE_CURSOR_OPENDOOR_IMAGE, directory="mouse_pointers")
        cblocals.global_mouseCursorType = type
    elif not type:
        cblocals.global_mouseCursor = cblocals.global_mouseCursorType = None
    else:
        raise ValueError("Cannot load cursor of type %s" % type)

def drawCursor(screen, (x, y) ):
    mouse_cursor = cblocals.global_mouseCursor
    x-= mouse_cursor.get_width() / 2
    y-= mouse_cursor.get_height() / 2
    screen.blit(mouse_cursor, (x,y))
# **********************

def loadAnimationByName(name, position, *containers):
    """Try to load an animation sprite know to the application.
    This method know how big is the animation size.
    """
    if name=='water-wave':
        from cheeseboys.sprites import WaterWave
        return WaterWave(position, (120,80), *containers)
    if name=='thunders':
        from cheeseboys.sprites import Thunders
        return Thunders(position, cblocals.GAME_SCREEN_SIZE, *containers)
    if name=='lighting':
        from cheeseboys.sprites import Lighting
        return Lighting(position, (103, 652), *containers)
    if name=='dark-largestain':
        from cheeseboys.sprites import DarkLargeStain
        x,y = position
        return DarkLargeStain((x, y+21), (62, 42), *containers)
    else:
        raise ValueError("Value %s is not a know animation." % name)

# ******* TEXT UTILS *******
def _generateTextLengthException(text_too_long, max_length):
    return ValueError('Text "%s" is really too long for me to fit a max length of %s!' % (text_too_long, max_length))

def normalizeTextLength(text_too_long, font, max_length):
    """This function take a text too long and split it in a list of smaller text lines.
    The final text max length must be less/equals than max_length parameter, using the font passed.
    Return a list of text lines.
    """
    words = text_too_long.split(" ")
    words_removed = []
    tooLong = True
    txt1 = txt2 = ""
    while tooLong:
        try:
            words_removed.append(words.pop())
        except IndexError:
            raise _generateTextLengthException(text_too_long, max_length)
        txt1 = " ".join(words)
        if font.size(txt1)[0]<=max_length:
            tooLong = False
    words_removed.reverse()
    txt2 = " ".join(words_removed)
    if txt2==text_too_long:
        raise _generateTextLengthException(text_too_long, max_length)
    if font.size(txt2)[0]<=max_length:
        return [txt1, txt2]
    else:
        return [txt1] + normalizeTextLength(txt2, font, max_length)
# **************

def update_version():
    """Check for a new version of the game"""
    import socket
    import urllib
    import xml.dom.minidom
    socket.setdefaulttimeout(10) # connection timeout
    stream = urllib.urlopen(cblocals.URL_CHEESEBOYS_LAST_VERSION)
    dom = xml.dom.minidom.parse(stream)
    stream.close()
    root = dom.getElementsByTagName('cheeseboys-version')[0]
    date = root.getElementsByTagName('date')[0].firstChild.nodeValue
    print date

