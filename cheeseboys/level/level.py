# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *
from cheeseboys import cblocals, utils
from cheeseboys.cbrandom import cbrandom
from cheeseboys.utils import Vector2
from cheeseboys.pygame_extensions import GameSprite, GameGroup
from cheeseboys.sprites import PhysicalBackground, Rain
from cheeseboys.presentation import Presentation
from level_text import LevelText

class GameLevel(object):
    """This repr a game level.
    Character move inside a level using some of its methods.
    
    When the level is draw, after the background image, all groups stored in this level
    are drawn ordered by zindex info.
    
    A GameLevel object can store a lot of groups; those groups (of time GameGroup) can be updatable or not.
    When a level is updated - calling the update(time_passed) method - on all groups of updatable tipe is
    called the update method.
    """
    
    def __init__(self, name, size, background=""):
        """Init a level object with a name and a size.
        If a background file name is given, this image is loaded as background.
        If you don't give a background then the level name (converted in a lowecase, less separated png file name)
        is used instead.
        If you really don't have a level image, please use a background parameter to None
        """
        self.name = name
        self.levelSize = size
        if background == '':
            background = name.lower().replace(" ","-")+".png"
        if background:
            self._background = utils.load_image(background, directory="levels")
        else:
            self._background = None
        self._topleft = (0,0)
        self._centeringSpeed = 50
        self._centeringHeading = None
        self._groups = []
        self._groups_toupdate = []
        self._groups_todraw = []
        self._rain = None
        self.screenReferenceSprite = None
        self.hero = None
        self.timeIn = 0.
        self.shadow = True
        
        # The presentation object running
        self.presentation = None
        self.level_text = None
        
        # This index will act on the ability of characters to hide in shadows in the level
        self.stealthLevel = 1.
        
        # Groups!
        all = GameGroup("all")
        dead = GameGroup("dead", drawable=True, updatable=True)
        physical = GameGroup("physical", drawable=True, updatable=True)
        charas = GameGroup("charas")
        enemies = GameGroup("enemies")
        animations = GameGroup("animations", drawable=True, updatable=True)
        top_animations = GameGroup("top_animations", drawable=True, updatable=True)
        speech = GameGroup("speech", updatable=True)            # speechs are handled in a special way
        level_text = GameGroup("level_text")
        exits = GameGroup("exits", drawable=True, updatable=True)
        triggers = GameGroup("triggers", drawable=True, updatable=True)
        tippable = GameGroup("tippable")                        # Tips are handled in a special way
        self.addGroup(all)
        self.addGroup(dead, zindex=5)
        self.addGroup(physical, zindex=10)
        self.addGroup(charas, zindex=10)
        self.addGroup(enemies)
        self.addGroup(animations, zindex=3)
        self.addGroup(top_animations, zindex=20)
        self.addGroup(speech)
        self.addGroup(level_text, zindex=30)
        self.addGroup(exits, zindex=3)
        self.addGroup(triggers, zindex=4)
        self.addGroup(tippable)

    def __getitem__(self, key):
        """Get a group by its name, or look for a GameSprite with that name if no group is found.
        """
        for group in self._groups:
            if group[1].name==key:
                return group[1]
        # not found a group; check for a GameSprite
        for group in self._groups:
            for sprite in group[1].sprites():
                if sprite.name==key:
                    return sprite
        raise KeyError("Not found group or sprite named '%s'" % key)

    def _setTopLeft(self, topleft):
        self._topleft = self._normalizeDrawPart(topleft)
    topleft = property(lambda self: self._topleft, _setTopLeft, doc="""The topleft drawing point inside the level background image""")
    
    @property
    def midbottom(self):
        """Midbottom of the screen on the level"""
        return self.rect.midbottom

    @property
    def rect(self):
        """A pygame.Rect from the level topleft, with the screen size"""
        return pygame.Rect(self.topleft, cblocals.GAME_SCREEN_SIZE)

    @property
    def center(self):
        """The point at the center of the drawn level part"""
        return self.rect.center

    def addGroup(self, group, zindex=10):
        """Add a new group the this level.
        All group are added to a default zindex info of 10.
        """
        self._groups.append( (zindex,group) )
        self._groups.sort(lambda x,y: x[0]-y[0])
        if group.updatable:
            self._groups_toupdate.append( (zindex,group) )
            self._groups_toupdate.sort(lambda x,y: x[0]-y[0])
        if group.drawable:
            self._groups_todraw.append( (zindex,group) )
            self._groups_todraw.sort(lambda x,y: x[0]-y[0])     
    
    def generateRandomPoint(self, fromPoint=(), maxdistance=0):
        """Generate a random point on the level.
        You can use this giving a distance and a start point to get a random point near that position.
        Normally the point is taken at random on level size.
        """
        if fromPoint and maxdistance:
            offset_x = cbrandom.randint(-maxdistance,maxdistance)
            offset_y = cbrandom.randint(-maxdistance,maxdistance)
            startX = fromPoint[0] - maxdistance
            endX = fromPoint[0] + maxdistance
            startY = fromPoint[1] - maxdistance
            endY = fromPoint[1] + maxdistance
        else:
            # If one of the not required param is missing, always use the normal feature
            startX = 1
            endX = self.levelSize[0]-1
            startY = 1
            endY = self.levelSize[1]-1
        return self.normalizePointOnLevel(cbrandom.randint(startX,endX), cbrandom.randint(startY,endY))

    def normalizePointOnLevel(self, x, y):
        """Given and x,y pair, normalize this to make this point valid on level coordinates"""
        if x<1: x=1
        elif x>self.levelSize[0]-1: x=self.levelSize[0]-1
        if y<1: y=1
        elif y>self.levelSize[1]-1: y=self.levelSize[1]-1 
        return x,y

    def normalizeRectOnScreen(self, rect):
        """Given a rect, make this rect is always contained in the screen"""
        w,h = cblocals.GAME_SCREEN_SIZE
        if rect.left<0:
            rect.left = 0
        if rect.right>w:
            rect.right = w
        if rect.top<0:
            rect.top = 0
        if rect.bottom>h:
            rect.bottom = h
        return rect

    def checkPointIsValidOnLevel(self, point, screenCoordinate=False):
        """Check if a coordinate is valid in current level.
        If screenCoordinate is True, then x,y will be normalized to level coord before use
        (calling transformToLevelCoordinate).
        """
        if screenCoordinate:
            x,y = self.transformToLevelCoordinate(point)
        if x<1: return False
        elif x>self.levelSize[0]-1: return False
        if y<1: return False
        elif y>self.levelSize[1]-1: return False 
        return True

    def checkRectIsInLevel(self, r):
        """Check if a rect is inside the level area"""
        levelRect = pygame.Rect( (0,0), self.levelSize)
        return levelRect.contains(r)

    def addSprite(self, sprite, firstPosition=None):
        """Add a sprite to this level at given position"""
        if not firstPosition:
            firstPosition = sprite.position
        sprite.addToGameLevel(self, firstPosition)
        # I memoize here sprites that use tips; tip can be evaluated False but not None
        if sprite.getTip() is not None:
            self['tippable'].add(sprite)

    def getCloserEnemy(self, character):
        """Return an enemy in the character sight range, or None"""
        sight = character.sightRange
        group = self['charas']
        enemies = []
        for charas in group.sprites():
            distanceFromCharas = character.distanceFrom(charas)
            if character.side!=charas.side and distanceFromCharas<=sight:
                if charas.stealth:
                    # A rogue charas reduce the character sight range
                    if distanceFromCharas <= int(sight * charas.getPreySightRangeReductionFactor()):
                        # ... and now the real check for the anti-stealth
                        if character.check_antiStealth(charas):
                            enemies.append(charas)
                else:    
                    enemies.append(charas)
        if enemies:
            return cbrandom.choice(enemies)
        return None

    def draw(self, screen):
        """Draw the level"""
        # 1 * Draw the background image
        if self._background:
            screen.blit(self._background.subsurface(pygame.Rect(self.topleft, cblocals.GAME_SCREEN_SIZE) ), (0,0) )
        # 2 * Draw all sprite groups
        for group in self._groups_todraw:
            group[1].draw(screen)
        # 3 * Draw screen center (if in DEBUG mode)
        if cblocals.DEBUG:
            xy, wh = self._getScreenCenter()
            xy = self.transformToScreenCoordinate(xy)
            pygame.draw.rect(screen, (50,250,250), (xy, wh), 2)
        self.drawRain(screen)
        # Special use of the level_text group
        if self['level_text']:
            self['level_text'].draw(screen)

    def update(self, time_passed):
        """Call the group update method on all (updatable) groups stored in this level"""
        for group in self._groups_toupdate:
            group[1].update(time_passed)
        if self._rain:
            self._rain.update(time_passed)
        self.timeIn+=time_passed

    def update_text(self, time_passed):
        """An update method that only works with the 'level_text' group"""
        if len(self['level_text'])>0:
            self['level_text'].update(time_passed)
            return True
        return False

    def _normalizeDrawPart(self, topleft=None, size=None):
        """Called to be sure that the draw portion of level isn't out of the level total surface"""
        x,y = topleft or self._topleft
        w,h = size or self.levelSize
        sw, sh = cblocals.GAME_SCREEN_SIZE
        if x<0:
            x=0
        if y<0:
            y=0
        if x+sw>w:
            x = w-sw
        if y+sh>h:
            y = h-sh
        return x,y
        
    def hasBackground(self):
        """Check is this level has a background image"""
        return self._background is not None

    def generateDeadSprite(self, corpse):
        """Using a character (commonly... very commonly... a DEAD ones!), generate a corpse.
        Corpse is added to a group called "dead".
        """
        sprite = GameSprite()
        sprite.image = utils.getRandomImageFacingUp(corpse.images)
        curRect = corpse.rect
        newRect = pygame.Rect( curRect.topleft, sprite.image.get_rect().size )
        newRect.midbottom = corpse.position
        sprite.rect = newRect
        self["dead"].add(sprite)
        sprite.addToGameLevel(self, corpse.position)

    def normalizeDrawPositionBasedOn(self, reference, time_passed):
        """Slowly move drawn portion of the total level, for centering it on the given reference object.
        reference can be a GameSprite or a position tuple info.
        """
        if pygame.key.get_pressed()[K_LCTRL]:
            return
        if type(reference)==tuple:
            referencePointOnScreen = reference
        else:
            referencePointOnScreen = reference.position_int
        if self.isPointAtScreenCenter(referencePointOnScreen, (200,200) ):
            return
        heading = Vector2.from_points(self.center, referencePointOnScreen)
        # More near to screen border, faster will be the screen centering procedure
        speed = self._centeringSpeed
        magnitude = heading.get_magnitude()
        if magnitude<120:
            pass
        elif magnitude<150:
            speed = speed*3
        elif magnitude<200:
            speed = speed*5
        elif magnitude>=250:
            speed = speed*6                        
        
        heading.normalize()
        distance = time_passed * speed
        movement = heading * distance
        x = movement.get_x()
        y = movement.get_y()
        self.topleft = (self.topleft[0]+x,self.topleft[1]+y)

    def _getScreenCenter(self, centerSize=(200,200)):
        """Return the screen center rect as ( (x,y), (w,h) )
        w and h are taken by the optional centerSize param.
        """
        cx, cy = self.center
        return (cx-centerSize[0]/2,cy-centerSize[1]/2), centerSize

    def isPointAtScreenCenter(self, refpoint, centerSize=(200,200)):
        """This method return true if a given point is inside a rect of given size.
        The rect is placed at the screen center
        """
        cx, cy = self.center
        rect = pygame.Rect( self._getScreenCenter(centerSize) )
        return rect.collidepoint(refpoint)

    def transformToLevelCoordinate(self, position):
        """Given a screen coordinate, transform it to level absolute position"""
        x, y = position
        tx, ty = self.topleft
        return (int(tx+x), int(ty+y))
    
    def transformToScreenCoordinate(self, position):
        """Given an level coordinate, transform it to screen position"""
        x, y = position
        tx, ty = self.topleft
        return (x-tx, y-ty)

    def addPhysicalBackground(self, position, size, groups=['physical']):
        """Add a PhysicalBackground instance to the current level.
        Use groups param to add the sprite to some groups stored in the level also.
        See PhysicalBackground for more info.
        """
        pb = PhysicalBackground( position, size )
        for group_name in groups:
            group = self[group_name]
            group.add(pb)
            self.addSprite(pb, position)
            
    def addAnimation(self, position, animation, groups=['animations']):
        """Add an animation sprite to this level.
        If animation parameter is a string, the engine try to load an animation with that name.
        """
        if type(animation)==str:
            animation = utils.loadAnimationByName(animation, position)    
        for group_name in groups:
            group = self[group_name]
            group.add(animation)
            # some animation can change original position
            if animation.position:
                position = animation.position
            self.addSprite(animation, position)

    def addAnimations(self, positions, animation, groups=['animations']):
        """Service method for call addAnimation multiple times, for fast add the same animation in many
        places on the level.
        """
        for position in positions:
            self.addAnimation(position, animation, groups=groups)

    def enableRainEffect(self):
        """Enable the rain effects in this level"""
        self._rain = Rain(self.levelSize)

    def drawRain(self, surface):
        """Draw the rain effect on the surface passed.
        This call do something only if the level has inited the rain effect calling GameLevel.enableRainEffect()
        """
        if self._rain:
            self._rain.draw(surface)

    def enablePresentation(self, presentation, presentation_dir="data/presentations"):
        """Load a presentation using its name and return a Presentation object.
        Also store current level presentation
        """
        if not presentation.endswith(".cbp"):
            presentation+=".cbp"
        pp = Presentation(self, presentation, presentation_dir=presentation_dir)
        self.presentation = pp
        pp.enablePresentationMode()
        return pp

    
    # ******* Level text methods *******
    def _useLevelText(self, text, type=cblocals.LEVEL_TEXT_TYPE_NORMAL):
        level_text = self.level_text
        if not level_text:
            level_text = LevelText(self, text, type)
            level_text.addToGameLevel(self, level_text.position)
            self.level_text = level_text
        else:
            level_text.addText(text)

    def levelTextIntro(self, text, colophon_flag=False):
        self._useLevelText(text, type=cblocals.LEVEL_TEXT_TYPE_BLACKSCREEN)
        if colophon_flag:
            self.level_text.colophon = True

    def levelText(self, text):
        self._useLevelText(text)
    # ******* /Level text methods *******

    def displayTip(self, surface, tip_sprite):
        """Display a GameSprite's tip on the surface, and control the tip position"""
        tip_structure = tip_sprite.getTip()
        if not tip_structure:
            return
        text = tip_structure['text']
        color = tip_structure['color']
        font = tip_structure.get('font',cblocals.default_font)
        background = tip_structure.get('background',None)
        fw,fh = font.size(text)
        rect = tip_sprite.physical_rect
        x,y = rect.midtop
        x=x-fw/2
        y=y-fh
        font_rect = pygame.Rect( (x,y),(fw,fh) )
        # Draw sprites's tip only if sprite is inside the screen
        if self.rect.colliderect(rect.move(self.topleft)):
            font_rect = self.normalizeRectOnScreen(font_rect)
            tip = font.render(text, True, color)
            if background:
                pygame.draw.rect(surface, background, font_rect, 0)
            surface.blit(tip, font_rect.topleft)


    def blitShadow(self, surface, refSprite):
        """Blit game general shadow.
        If the shadow has a light area, its based on a reference sprite.
        Do nothing if GameLevel.shadow is False"""
        if self.shadow:
            if not self.presentation:
                if not refSprite.outOfScreen:
                    spriteposx, spriteposy = self.transformToScreenCoordinate(refSprite.position)
                    imgsizew,imgsizeh = cblocals.SHADOW_IMG_SIZE
                    surface.blit(cblocals.shadow_image, (spriteposx-imgsizew/2, spriteposy-imgsizeh/2))
                else:
                    surface.blit(cblocals.total_shadow_image_09, (0,0) )
            else:
                surface.blit(cblocals.total_shadow_image_05, (0,0) )
