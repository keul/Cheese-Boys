# -*- coding: utf-8 -

import pygame
from pygame.locals import *

from cheeseboys import cblocals, utils
from cheeseboys.cbrandom import cbrandom
from cheeseboys.ai import PresentationStateMachine
from cheeseboys.utils import Vector2
from cheeseboys.pygame_extensions import GameSprite
from cheeseboys.attack import Attack
from cheeseboys.th0 import TH0
from cheeseboys.sprites import SpeechCloud

class Character(GameSprite):
    """Base character class.
    A GameSprite extension with hit points and other properties for combat.
    """

    _imageDirectory = "charas"
    
    def __init__(self, name, img, containers,
                 realSize=cblocals.TILE_IMAGE_DIMENSION, speed=150., attackTime=0.5, afterAttackRestTime=0.2, weaponInAndOut=False, sightRange=200,):
        
        GameSprite.__init__(self, *containers)
        self._x = self._y = 0
        self.rect = pygame.Rect( (self.x, self.y), (cblocals.TILE_IMAGE_DIMENSION) )

        self.name = name
        self.characterType = "Guy"
        
        self._brain = None
        self._presentationBrain = PresentationStateMachine(self)
        
        self._load_images(img, weaponInAndOut)
        self.lastUsedImage = 'head_south_1'

        self._distanceWalked = 0
        self._mustChangeImage = False
        self.direction = self._lastUsedDirection = cblocals.DIRECTION_S
        self._isMoving = False
        self.maxSpeed = self.speed = speed
        self.sightRange = sightRange
        self.rest_time_needed = .3
        
        self.side = 'Cheese Boys'
        self._enemyTarget = None
        
        self._navPoint = None
        self.heading =  None

        # Attack infos
        self._attackDirection = None
        self.attackHeading = self.lastAttackHeading = None
        self._attackRange = 24
        self._attackEffect = 10
        self._attack = None
        self._attackColor = (255, 255, 255, 200)
        self._attackLineWidth = 2
        self._attackTimeCollected = self._attackAnimationTimeCollected = 0
        self._attackTime = attackTime
        self._afterAttackRestTime = afterAttackRestTime
        self._attackAnimationTime = attackTime/2
        self.attackDamage = "1d6"
        
        # From where a succesfull attack is coming
        self.damageHeading = None
        
        self.dimension = realSize
        self._heatRectData = (5, 5, 10,15)

        self.hitPoints = self.hitPointsLeft = 20
        
        self._baseAC = 1
        self._th0 = None

        self._speech = SpeechCloud(self)

        self.afterInit()

    def afterInit(self):
        """Called after object creation to do something more specific for different character
        I don't want to overload the __init__ method.
        Base form of this method do nothing at all!
        """
        pass

    def setCombatValues(self, level_bonus, AC):
        """Common method for set all combat infos of the character, as far as base AC and TH0 infos are readonly"""
        self._th0 = TH0(level_bonus)
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
    
    def roll_for_hit(self, target):
        """Common method called to rool a dice and see if a target is hit by the blow"""
        th0 = self._th0
        targetAC = target.AC
        result = th0.attack(targetAC)
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
        self.heading.normalize()
        direction = self._generateDirectionFromHeading(self.heading)
        self._checkDirectionChange(direction)

        self.moving(True)
        distance = time_passed * self.speed
        movement = self.heading * distance
        self.addDistanceWalked(distance)
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
        """This is similar to moveBasedOnNavPoint, but is called to animate a character that wanna retreat"""
        heading = -self.heading
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
        # BBB: some bigger or different images can behave other rect as "foot"?
        """
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
        diffW = rect.w-self.dimension[0]
        diffH = rect.h-self.dimension[1]
        return pygame.Rect( (rect.left+diffW/2, rect.top+diffH), self.dimension )

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
        BBB: I need a way to memoize this!!!!
        """
        if self._attackDirection:
            weaponOut = True
        else:
            weaponOut = False

        if self._isMoving:
            # I'm on move
            if self._mustChangeImage:
                if self._attackDirection:
                    direction = self._attackDirection
                else:
                    direction = self._lastUsedDirection
                self._mustChangeImage = False
                image = self._getImageFromDirectionWalked(direction, weaponOut)
                self.lastUsedImage = image
            return self.images[self.lastUsedImage]
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
            return self.images[image]

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
        # BBB

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

    def addDistanceWalked(self, distance):
        self._distanceWalked+=distance
        # Every MIN_PX_4_IMAGES_CHANGEpx change image to simulate footsteps.
        # BBB: ugly for very slow charas
        if self._distanceWalked>=cblocals.MIN_PX_4_IMAGES_CHANGE:
            self._distanceWalked=0
            self._mustChangeImage = True

    def _checkDirectionChange(self, direction):
        """Check if the character movement direction is changed"""
        if direction!=self._lastUsedDirection:
            self._lastUsedDirection = direction
            self._mustChangeImage = True

    def walk(self, distance, direction=None):
        """Walk the character to a direction
        BBB: not used anymore; Delete this?
        """
        if not direction:
            direction = self.direction
        if not self._isMoving:
            return
        
        self.addDistanceWalked(distance)
        self._checkDirectionChange(direction)

        if direction==cblocals.DIRECTION_E:
            self.move(distance, 0)
        elif direction==cblocals.DIRECTION_S:
            self.move(0, distance)
        elif direction==cblocals.DIRECTION_W:
            self.move(-distance,0)
        elif direction==cblocals.DIRECTION_N:
            self.move(0, -distance)
        elif direction==cblocals.DIRECTION_NE:
            self.move(distance, -distance)
        elif direction==cblocals.DIRECTION_SE:
            self.move(distance, distance)
        elif direction==cblocals.DIRECTION_SW:
            self.move(-distance, distance)
        elif direction==cblocals.DIRECTION_NW:
            self.move(-distance, -distance)

    def setAttackState(self, heading):
        """Set the character attack versus an heading direction.
        For duration of the attack the character can still moving, but will face the direction attacked.
        """
        direction = self._generateDirectionFromHeading(heading)
        self.attackHeading = self.lastAttackHeading = heading
        self._attackDirection = direction
        self._mustChangeImage = True

    def updateAttackState(self, time_passed):
        """Called to add some time to the attack time.
        This method control how long the attack is in action.
        """
        if self._attackTimeCollected<self._attackTime + self._afterAttackRestTime:
            self._attackTimeCollected+=time_passed
        else:
            self.stopAttack()

    def drawAttack(self, surface, time_passed):
        """Draw an attack effect on a surface in the attack heading direction.
        This method do nothing if isAttacking method return False.
        First this method get a point (call this attackEffectCenterVector) using the heading of the attack
        far from the character by a value equals to _attackRange/2 property of this character.
        This attackEffectCenterVector is a point from which we draw an X, thar repr charas attack.
        """
        if not self.isAttacking():
            return

        attackOriginVector = Vector2(self.physical_rect.center)
        if not self._attack:
            self._attack = Attack(self, attackOriginVector, self._attackRange, self._attackEffect, self._attackColor, self._attackLineWidth)

        self._attackAnimationTimeCollected+=time_passed
        if self._attackAnimationTimeCollected<self._attackAnimationTime/2:
            self._attack.drawPhase1(surface, attackOriginVector)
        elif self._attackAnimationTimeCollected<self._attackAnimationTime:
            self._attack.drawPhase2(surface, attackOriginVector)
        # else pass

    def isAttacking(self):
        """Test if this charas is making an attack"""
        if self.attackHeading:
            return True
        return False

    def stopAttack(self):
        """Stop attack immediatly, resetting all attack infos"""
        self._attackDirection = self.attackHeading = self._attack = None
        self._attackTimeCollected = self._attackAnimationTimeCollected = 0

    def moving(self, new_move_status):
        """Change character movement status"""
        if new_move_status!=self._isMoving:
            self._mustChangeImage = True
        self._isMoving = new_move_status

    def setNavPoint(self, xy):
        """Set a new target navPoint for current character"""
        if isinstance(xy, Vector2):
            self.navPoint = xy
        else:
            self.navPoint = Vector2(xy)

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
    def attackRange(self):
        """The range of the character's attacks"""
        return self._attackRange

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
        """Kill the character, removing it from all groups"""
        GameSprite.kill(self)
        self.currentLevel.generateDeadSprite(self)

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

    def generatePhysicalAttachEffect(self, attack_origin, criticity=None):
        """Called for animate a character hit by a physical blow.
        Character will innaturally move away in a direction opposite to blow origin.
        """
        damage = cbrandom.throwDices(attack_origin.attackDamage)
        critic = ""
        if criticity and criticity==cblocals.TH0_HIT_CRITICAL:
            if cbrandom.randint(1,2)==1:
                self.shout(_("Ouch!"))
            damage = int(damage * 1.5)
            critic = "CRITICAL! "
        self.hitPointsLeft-= damage
        print "  %s%s wounded for %s points. %s left" % (critic, self.name, damage, self.hitPointsLeft)
        # Below I use lastAttackHeading because may be that attackHeading is now None (enemy ends the attack)
        self.damageHeading = attack_origin.lastAttackHeading
        if self.brain:
            self.brain.setState("hitten")
        if not self.checkAliveState():
            print "%s is dead." % self.name

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
        event = pygame.event.Event(cblocals.SHOUT_EVENT, {'character':self, 'position':self.position, 'text': text})
        pygame.event.post(event)

    def shutup(self):
        """Immediatly shut up the character"""
        self._speech.endSpeech()

    def __str__(self):
        return "Character %s" % self.name

