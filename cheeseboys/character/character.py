# -*- coding: utf-8 -

import logging

import pygame
from pygame.locals import *

from cheeseboys import cblocals, utils
from cheeseboys.cbrandom import cbrandom
from cheeseboys.ai import PresentationStateMachine
from cheeseboys.ai.pathfinder import PathFinder
from cheeseboys.utils import Vector2
from cheeseboys.pygame_extensions.sprite import GameSprite
from cheeseboys import th0 as module_th0
from cheeseboys.sprites import SpeechCloud

from stealth import Stealth
from warrior import Warrior

class Character(GameSprite, Stealth, Warrior):
    """Base character class.
    A GameSprite extension with hit points and other properties for combat.
    """

    _imageDirectory = "charas"
    
    def __init__(self, name, img, containers,
                 realSize=cblocals.TILE_IMAGE_SIZE, speed=150.,
                 attackTime=0.5, afterAttackRestTime=0.2, weaponInAndOut=False, sightRange=200,):
        
        GameSprite.__init__(self, *containers)
        Stealth.__init__(self)
        Warrior.__init__(self, attackTime, afterAttackRestTime)

        self._x = self._y = 0
        self.rect = pygame.Rect( (self.x, self.y), (cblocals.TILE_IMAGE_SIZE) )

        self.name = name
        self.characterType = "Guy"
        self.experienceLevel = 1
        
        self._brain = None
        self._presentationBrain = PresentationStateMachine(self)
        
        self._load_images(img, weaponInAndOut)
        self.lastUsedImage = 'head_south_1'

        self._stepTime = 0
        self._mustChangeImage = False
        self.direction = self._lastUsedDirection = cblocals.DIRECTION_S
        self._isMoving = False
        self.maxSpeed = self._speed = speed
        self.sightRange = sightRange
        self.rest_time_needed = .3
        
        self.side = 'Cheese Boys'
        self._enemyTarget = None
        
        self._navPoint = None
        self.heading =  None
        
        # From where a succesfull attack is coming
        self.damageHeading = None
        
        self.size = realSize
        self._heatRectData = (5, 5, 10,15)

        self.hitPoints = self.hitPointsLeft = 20
        
        self._baseAC = 1
        self._th0 = None

        self._speech = SpeechCloud(self)
        
        # *** Pathfinding ***
        self.pathfinder = None        # This is inited only after the call onto addToGameLevel
        self.computed_path = []

        self.afterInit()

    def afterInit(self):
        """Called after object creation to do something more specific for different character
        I don't want to overload the __init__ method.
        Base form of this method do nothing at all!
        """
        pass

    def _setSpeed(self, speed):
        self._speed = speed
    def _getSpeed(self):
        speed = self._speed
        healtFactor = self.healtFactor
        if self.stealth:
            speed*=.5
        if healtFactor<.2:
            speed*=.6
        elif healtFactor<.5:
            speed*=.8
        return int(speed)
    speed = property(_getSpeed, _setSpeed, doc="""The character current movement speed""")

    @property
    def isMoving(self):
        return self._isMoving

    def setCombatValues(self, level_bonus, AC):
        """Common method for set all combat values of the character, as far as base AC and TH0 infos are readonly"""
        self._th0 = module_th0.TH0(self, level_bonus)
        self._baseAC = AC

    def _setNavPoint(self, value):
        if type(value)==tuple:
            value = Vector2(value)
        self._navPoint = value
    navPoint = property(lambda self: self._navPoint, _setNavPoint, doc="""The character navigation point""")

    @property
    def th0(self):
        return self._th0

    @property
    def AC(self):
        """The character current Armour Class value, based on a base value and some other status"""
        base_ac = self._baseAC
        bonus = 0
        active_state = self.active_state
        # BBB: may be very better query the state directly (with a getAcModifier method?)
        if active_state=="retreat":
            bonus = 4
        elif active_state=="attacking":
            bonus = -2
        return base_ac + bonus

    @property
    def healtFactor(self):
        """Service value to get a general healt value for the character.
        @return: a real value between 0 (dead) and 1 (100% healed)
        """
        return float(self.hitPointsLeft)/float(self.hitPoints)
    
    def roll_for_hit(self, target):
        """Common method called to rool a dice and see if a target is hit by the blow"""
        th0 = self._th0
        result = th0.attack(target)
        return result

    def getTip(self):
        """Return tip text, for print it near the character"""
        tip = self._emptyTipStructure.copy()
        tip['text']= self.name or self.characterType
        tip['color']=(255,255,255)
        return tip

    def _load_images(self, img, weaponInAndOut):
        """Load images for this charas: 12 or 24 if used weaponInAndOut (so we need extra images without weapon)"""
        self.images = {}
        directory = self._imageDirectory
        if not weaponInAndOut:
            # 12 images
            self.images['walk_north_1'], self.images['head_north'], self.images['walk_north_2'], self.images['walk_east_1'], \
                self.images['head_east'], self.images['walk_east_2'], self.images['walk_south_1'], self.images['head_south'], \
                self.images['walk_south_2'], self.images['walk_west_1'], self.images['head_west'], \
                self.images['walk_west_2'] = utils.load_image(img, directory, charasFormatImage=True, weaponInAndOut=weaponInAndOut)
        else:
            # 24 images
            self.images['walk_north_1'], self.images['head_north'], self.images['walk_north_2'], self.images['walk_east_1'], \
                self.images['head_east'], self.images['walk_east_2'], self.images['walk_south_1'], self.images['head_south'], \
                self.images['walk_south_2'], self.images['walk_west_1'], self.images['head_west'], \
                self.images['walk_west_2'], \
                self.images['attack_north_1'], self.images['head_attack_north'], self.images['attack_north_2'], self.images['attack_east_1'], \
                self.images['head_attack_east'], self.images['attack_east_2'], self.images['attack_south_1'], self.images['head_attack_south'], \
                self.images['attack_south_2'], self.images['attack_west_1'], self.images['head_attack_west'], \
                self.images['attack_west_2'] = utils.load_image(img, directory, charasFormatImage=True, weaponInAndOut=weaponInAndOut)

    @property
    def brain(self):
        """The brain of the character.
        This will be a PresentationStateMachine instance if a presentation is running
        """
        if self.currentLevel.presentation is not None:
            return self._presentationBrain
        return self._brain

    @property    
    def real_brain(self):
        """The brain of the character. Do not use this property but always the Character.brain.
        Use this only if you need to refer to the character's real brain when a presentation is running
        """
        return self._brain

    def update(self, time_passed):
        """Update method of pygame Sprite class.
        A non playing character check his own AI here.
        """
        GameSprite.update(self, time_passed)
        if self.brain:
            self.brain.think(time_passed)

    def moveBasedOnNavPoint(self, time_passed, destination=None, relative=False):
        """Main method for move character using navPoint infos.
        If a destination is not specified, then the current character navPoint is used.
        You can also specify a destination as relative coordinate starting from the current navPoint, using the
        relative parameter.
        """
        if not destination:
            destination = self.navPoint
        else:
            if type(destination)==tuple:
                if relative:
                    ox, oy = destination
                    cx, cy = self.position
                    destination = (cx+ox, cy+oy)
                destination = Vector2(destination)
            self.navPoint = destination
        self.heading = Vector2.from_points(self.position, destination)
        magnitude = self.heading.get_magnitude()
        self.heading.normalize()

        self.moving(True)
        distance = time_passed * self.speed
        # I don't wanna move over the destination!
        if distance>magnitude:
            distance = magnitude
        else:
            # I don't check for a new direction if I'm only fixing the last step distance
            direction = self._generateDirectionFromHeading(self.heading)
            self._checkDirectionChange(direction)

        movement = self.heading * distance
        self._updateStepTime(time_passed)
        x = movement.get_x()
        y = movement.get_y()
#        new_coord = self.getBestCoordinateToAvoidCollision(x,y)
#        if new_coord:
#            self.move(*new_coord)
        if not self.checkCollision(x, y):
            self.move(x, y)
            if self.isNearTo(self.navPoint.as_tuple()):
                self.navPoint = None
                self.moving(False)
        else:
            self.navPoint = None
            self.moving(False)

    def moveBasedOnHitTaken(self, time_passed):
        """This is similar to moveBasedOnNavPoint, but is called to animate a character hit by a blow"""
        distance = time_passed * self.speed
        movement = self.damageHeading * distance
        x = movement.get_x()
        y = movement.get_y()
        if not self.checkCollision(x, y) and self.checkValidCoord(x, y):
            self.move(x, y)

    def moveBasedOnRetreatAction(self, time_passed):
        """This is similar to moveBasedOnNavPoint, but is called to animate a character that wanna retreat.
        The movement is done in the direction opposite to the heading, but with an offeset of +/- 50° degree.
        """
        heading = -self.heading
        heading.rotate(cbrandom.randint(-50,50))
        distance = time_passed * self.speed
        movement = heading * distance
        x = movement.get_x()
        y = movement.get_y()
        if not self.checkCollision(x, y) and self.checkValidCoord(x, y):
            self.move(x, y)

    @property
    def collide_rect(self):
        """See GameSprite.collide_rect.
        for characters, the foot area is the 25% of the height and 60% in width of the charas, centered on the bottom.
        """
        # BBB: some bigger or different images can behave other rect as "foot"?
        rect = self.rect
        ly = rect.bottom
        h = rect.h*0.25
        hy = ly-h
        lx = rect.left + rect.w*0.2 # left + 20-left% of the width
        w = rect.w*0.6
        return pygame.Rect( (lx, hy), (w, h) )

    @property
    def physical_rect(self):
        """See GameSprite.physical_rect.
        Return a rect used for collision in combat (not movement).
        This must be equals to image's character total area.
        """
        rect = self.rect
        diffW = rect.w-self.size[0]
        diffH = rect.h-self.size[1]
        return pygame.Rect( (rect.left+diffW/2, rect.top+diffH), self.size )

    @property
    def heat_rect(self):
        """Return a rect used for collision as heat rect, sensible to attack and other evil effects.
        """
        physical_rect = self.physical_rect
        offsetX, offsetY, w, h = self._heatRectData
        return pygame.Rect( (physical_rect.x+offsetX, physical_rect.y+offsetY), (w, h) )

    def checkValidCoord(self, x=0, y=0):
        """Check if the character coords are valid for current Level
        You can also use x,y adjustement to check a different position of the character, relative
        to the current one.
        """
        r = self.physical_rect.move(x,y)
        r.center = self.currentLevel.transformToLevelCoordinate(r.center)
        return self.currentLevel.checkRectIsInLevel(r)
    
    @property
    def image(self):
        """Sprite must have an image property.
        In this way I can control what image return.
        """
        # BBB: I need a way to memoize this!!!!
        if self._attackDirection:
            weaponOut = True
        else:
            weaponOut = False

        if self._isMoving:
            # I'm on move
            if self._mustChangeImage:
                direction = self._getFacedDirection()
                self._mustChangeImage = False
                image = self._getImageFromDirectionWalked(direction, weaponOut)
                self.lastUsedImage = image
            return self._manageImageWithStealth(self.images[self.lastUsedImage])
        else:
            # Stand and wait
            if self._attackDirection:
                # I change the last faced direction because when I right click on a direction when the character isn't moving
                # I wanna turn in that direction.
                direction = self._lastUsedDirection = self._attackDirection
            else:
                direction = self._lastUsedDirection
            image = self._getImageFromDirectionFaced(direction, weaponOut)
            self.lastUsedImage = image
            return self._manageImageWithStealth(self.images[image])

    def _getFacedDirection(self):
        """If the character was attacking, the direction is the attack direction (_attackDirection).
        Otherwise use the common last used direction _lastUsedDirection.
        """
        if self._attackDirection:
            return self._attackDirection
        return self._lastUsedDirection

    def _manageImageWithStealth(self, image):
        """Calculate the alpha value for an image based on the charas stealth level"""
        alpha = 255*self.stealthIndex
        image.set_alpha(alpha)
        return image

    def faceTo(self, direction):
        """Change the character direction faced"""
        self._lastUsedDirection = direction

    def _generateDirectionFromHeading(self, new_heading):
        """Looking at heading, generate a valid direction string"""
        x, y = new_heading.as_tuple()
        if abs(x)<.30 and y<0:
            return cblocals.DIRECTION_N
        if abs(x)<.30 and y>0:
            return cblocals.DIRECTION_S
        if x<0:
            return cblocals.DIRECTION_W
        return cblocals.DIRECTION_E

    def _getWalkImagePrefix(self, direction, weaponOut):
        """Simply return a prefix using to generate the key to retrieve the charas image.
        This prefix is based on the direction of the character but also on the attack state.
        """
        if weaponOut:
            prefix = "attack"
        else:
            prefix = "walk"
        if direction==cblocals.DIRECTION_E or direction==cblocals.DIRECTION_NE or direction==cblocals.DIRECTION_SE:
            return "%s_east_" % prefix
        if direction==cblocals.DIRECTION_W or direction==cblocals.DIRECTION_NW or direction==cblocals.DIRECTION_SW:
            return "%s_west_" % prefix
        if direction==cblocals.DIRECTION_N:
            return "%s_north_" % prefix
        if direction==cblocals.DIRECTION_S:
            return "%s_south_" % prefix
        raise ValueError("Invalid direction %s" % direction)   
    
    def _getImageFromDirectionWalked(self, direction, weaponOut):
        """Using a direction taken get the right image name to display.
        This method check if an attack is currently executed by this character (checking weaponOut). If this is True
        we must return the image facing direction attacked.
        """
        imagePrefix = self._getWalkImagePrefix(direction, weaponOut)
        if self.lastUsedImage.startswith(imagePrefix):
            if self.lastUsedImage.endswith("1"):
                image = self.lastUsedImage[:-1]+"2"
            else:
                image = self.lastUsedImage[:-1]+"1"
        else:
            image = imagePrefix+"1"
        return image

    def _getImageFromDirectionFaced(self, direction, weaponOut):
        """Using a direction, chose the right character non-moving image.
        Use weaponOut to know if an image without weapong carried must be used.
        """
        if weaponOut:
            wstr = "attack_"
        else:
            wstr = ""
        if direction==cblocals.DIRECTION_E or direction==cblocals.DIRECTION_NE or direction==cblocals.DIRECTION_SE:
            image = "head_%seast" % wstr
        elif direction==cblocals.DIRECTION_W or direction==cblocals.DIRECTION_NW or direction==cblocals.DIRECTION_SW:
            image = "head_%swest" % wstr
        elif direction==cblocals.DIRECTION_N:
            image = "head_%snorth" % wstr
        elif direction==cblocals.DIRECTION_S:
            image = "head_%ssouth" % wstr
        else:
            raise ValueError("Invalid direction %s" % direction) 
        return image

    def _generateHeadingFromFacindDirection(self, direction):
        """Passed a direction, return a normalized Vector2 based on the faced direction"""
        if direction==cblocals.DIRECTION_N:
            return Vector2(0.,-1.)
        if direction==cblocals.DIRECTION_E:
            return Vector2(1.,0.)
        if direction==cblocals.DIRECTION_S:
            return Vector2(0.,1.)
        if direction==cblocals.DIRECTION_W:
            return Vector2(-1.,0.)
        raise TypeError("Invalid direction %s" % direction)

    def _updateStepTime(self, time_passed):
        """Update the time passed from the last step ot this character"""
        self._stepTime+=time_passed
        if self._stepTime>=cblocals.CHARAS_STEP_TIME:
            self._stepTime=0
            self._mustChangeImage = True

    def _checkDirectionChange(self, direction):
        """Check if the character movement direction is changed"""
        if direction!=self._lastUsedDirection:
            self._lastUsedDirection = direction
            self._mustChangeImage = True

    def moving(self, new_move_status):
        """Change character movement status"""
        if new_move_status!=self._isMoving:
            self._mustChangeImage = True
        if new_move_status==False:
            # When the character stops from moving, the character heading is changed by the direction faced
            direction = self._getFacedDirection()
            self.heading = self._generateHeadingFromFacindDirection(direction)
        self._isMoving = new_move_status

    def setBrain(self, smBrain):
        """Set a AI StateMachine istance"""
        self._brain = smBrain(self)

    def _set_braine_enabled(self, value):
        self._brain.enabled = value
    brain_enabled = property(lambda self: self._brain.enabled, _set_braine_enabled, doc="""The current character's brain status""")
  
    @property
    def active_state(self):
        """Get the current brain active state"""
        if self.brain:
            return self.brain.active_state.name
        return None
    
    def _setEnemyTarget(self, enemy):
        self._enemyTarget = enemy
    enemyTarget = property(lambda self: self._enemyTarget, _setEnemyTarget, doc="""The character current enemy target""")

    @property
    def isAlive(self):
        """True if the character is alive"""
        return self.hitPointsLeft>0

    def checkAliveState(self):
        """Check the character alive state, or kill it!
        In any case return the alive state as a boolean.
        """
        if not self.isAlive:
            self.kill()
            return False
        return True
    
    def kill(self):
        """Kill the character, removing it from all groups and draw a dead corpse.
        As far as the Character objects are also UniqueObject, we need also to
        unregister a killed sprite from the object_registry.
        """
        GameSprite.kill(self)
        self.currentLevel.generateDeadSprite(self)
        cblocals.object_registry.unregister(self.UID())

    def getHeadingTo(self, target):
        """Return the heading to a given object or position.
        Object must have a "position" attribute or be a position tuple itself.
        """
        if hasattr(target, 'position'):
            position = target.position
        else:
            position = target
        heading = Vector2.from_points(self.position, position)
        return heading.normalize()

    def generatePhysicalAttackEffect(self, attacker, criticity=None):
        """Called for animate a character hit by a physical blow.
        Character will innaturally move away in a direction opposite to blow origin.
        """
        damage = cbrandom.throwDices(attacker.attackDamage)
        critic = ""

        if criticity and criticity==module_th0.TH0_SURPRISE_HIT:
            critic = "BACKSTAB! "
            damage*=cbrandom.randint(3,4)
        elif criticity and criticity==module_th0.TH0_HIT_CRITICAL:
            if cbrandom.randint(1,2)==1:
                self.shout(_("Ouch!"))
            damage = int(damage * 1.5)
            critic = "CRITICAL! "
        elif criticity and criticity==module_th0.TH0_HIT_SURPRISE_CRITICAL:
            damage*=cbrandom.randint(4,6)
            critic = "DEADLY! "

        self.hitPointsLeft-= damage
        print "  %s%s wounded for %s points. %s left" % (critic, self.name, damage, self.hitPointsLeft)
        # Below I use lastAttackHeading because may be that attackHeading is now None (enemy ends the attack)
        self.damageHeading = attacker.lastAttackHeading
        if self.brain:
            self.brain.setState("hitten")
        if not self.checkAliveState():
            print "%s is dead." % self.name
        elif attacker.stealth and not self.canSeeHiddenCharacter(attacker):
            # The attacker was hidden in shadows and unseen, but the character (the target) is not dead! Now the character can see it!
            self.noticeForHiddenCharacter(attacker)
        # however the character has been hit, so I need to reset it's stealth state
        if self.stealth:
            self.stealth = False

    @classmethod
    def getHealtColor(cls, total, left):
        """Given two value return a tuple RBG that repr a color for points left.
        More point left, more the color will be green.
        With point decrease, this will lead to red.
        """
        # 255 : total = x : left
        v1 = 255*left/total
        return (255-v1,v1,0)

    def drawPointsInfos(self, surface):
        """Draw infos about this character point left on the surface"""
        hitPoints = self.hitPoints
        hitPointsLeft = self.hitPointsLeft
        pr = self.physical_rect
        # hitPoints : pr.height = hitPointsLeft : x
        topright = (pr.topright[0], pr.bottomright[1] - (pr.height * hitPointsLeft / hitPoints) )
        pygame.draw.line(surface, self.getHealtColor(hitPoints, hitPointsLeft), pr.bottomright, topright, 3)

    # Talking methods
    def say(self, text, additional_time=0, silenceFirst=False):
        """Say something, displaying the speech cloud"""
        if silenceFirst:
            self._speech.endSpeech()
        self._speech.text = text
        if additional_time:
            self._speech.additionalTime(additional_time)

    def shout(self, text, additional_time=0, silenceFirst=False):
        """As say() but with uppercase text"""
        if silenceFirst:
            self._speech.endSpeech()
        self._speech.text = text.upper()
        if additional_time:
            self._speech.additionalTime(additional_time)
        event = pygame.event.Event(cblocals.SHOUT_EVENT, {'character':self, 'position':self.position_int, 'text': text})
        pygame.event.post(event)

    def shutup(self):
        """Immediatly shut up the character"""
        self._speech.endSpeech()


    def hasFreeSightOn(self, sprite):
        """Return True if the target sprite is in sight of the current character"""
        to_target = Vector2.from_points(self.position, sprite.position)
        magnitude = to_target.get_magnitude()
        # 1 - False if sprite position is outside the character sight
        if self.sightRange<magnitude:
            return False
        # 2 - Now I need to get the line sight on the target
        to_target.normalize()
        magnitude_portion = max(magnitude/100., 15)
        visual_obstacles = self.currentLevel['visual_obstacles']
        screen_position = self.toScreenCoordinate()
        while magnitude>0:
            for obstacle in visual_obstacles:
                temp_v = (to_target*magnitude).as_tuple()
                temp_pos = screen_position[0]+temp_v[0], screen_position[1]+temp_v[1]
                #print temp_pos, obstacle.rect
                if obstacle.collide_rect.collidepoint(temp_pos):
                    logging.debug("%s can't see %s due to the presence of %s" % (self, sprite, obstacle))
                    return False
            magnitude-=magnitude_portion
        return True

    def addToGameLevel(self, level, firstPosition):
        """Call the GameSprite.addToGameLevel but also init the pathfinder object"""
        GameSprite.addToGameLevel(self, level, firstPosition)
        self.pathfinder = PathFinder(self.currentLevel.grid_map_successors,
                                     self.currentLevel.grid_map_move_cost,
                                     self.currentLevel.grid_map_heuristic_to_goal)

    def compute_path(self):
        """Call PathFinder.compute_path using the character position as start point
        and his navPoint as goal"""
        if self.navPoint:
            goal = self.currentLevel.toGridCoord(self.navPoint.as_tuple())
            self.computed_path = self.pathfinder.compute_path(self.position_grid, goal)
        else:
            self.computed_path = []
        return self.computed_path

    def __str__(self):
        return "%s <%s>" % (self.name, self.UID())

    def __repr__(self):
        return str(self)
