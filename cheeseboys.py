#! /usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys, logging, optparse
import gettext

# CHECKING GAME DEPENDENCIES
print "Checking dependencies..."
try:
    import pygame
    print "Pygame library found."
except ImportError:
    print ("Pygame module isn't present!\n"
           "This is the main game module! You must download it from\n"
           "http://pygame.org/download.shtml")
    sys.exit(1)

# Check for pygame 1.8
print "Checking for pygame version..."
from pygame import version
if version.vernum[0]<2 and version.vernum[1]<8:
    print ("WARNING: your pygame version is %s\n"
           "Cheese Boys rely on pygame 1.8.1, or a better version.\n")  % version.ver
else:
    print "Found pygame %s. OK..." % version.ver 

# Checking for KezMenu
try:
    import kezmenu
    print "KezMenu library found."
except ImportError:
    print ("KezMenu module isn't present!\n"
           "This is used for Cheese Boys's menu interfaces! You must download it from\n"
           "http://pypi.python.org/pypi/KezMenu/\n"
           "or simply install it with easy_install typing\n"
           "  easy_install KezMenu")
    sys.exit(1)

# Checking for KezMenu
try:
    import ktextsurfacewriter
    print "KTextSurfaceWriter library found."
except ImportError:
    print ("KTextSurfaceWriter module isn't present!\n"
           "This is required library for Cheese Boys! You must download it from\n"
           "http://pypi.python.org/pypi/KTextSurfaceWriter/\n"
           "or simply install it with easy_install typing\n"
           "  easy_install KTextSurfaceWriter")
    sys.exit(1)

print "All required libraries are present."
# #######

os.environ['SDL_VIDEO_CENTERED'] = '1'
from pygame.locals import *

from cheeseboys import cblocals, utils, character
from cheeseboys import th0 as module_th0
from cheeseboys.pygame_extensions import GameSprite
from cheeseboys.pygame_extensions.unique import UniqueObjectRegistry
from cheeseboys.level import loadLevelByName
from cheeseboys.ai.hero import HeroStateMachine

def handleFullScreen():
    if cblocals.FULLSCREEN:
        screen = pygame.display.set_mode(cblocals.SCREEN_SIZE, FULLSCREEN, 32)
    else:
        screen = pygame.display.set_mode(cblocals.SCREEN_SIZE, 0, 32)
    cblocals.screen = screen
    return screen

def game():
    
    clock = pygame.time.Clock()
    screen = cblocals.screen

    hero = character.PlayingCharacter("The Hero", ("hero_sword1_vest1.png","hero_vest1.png"), (), realSize=(18,25), weaponInAndOut=True)
    hero.setBrain(HeroStateMachine)
    hero.setCombatValues(2, 13)

    level = loadLevelByName("The South Bridge", hero)
    level.enablePresentation('funny-intro')
    
    pygame.display.set_caption("Cheese Boys (alpha release) %s - %s" % (cblocals.__version__, level.name))

    console_area = pygame.Surface( cblocals.CONSOLE_SCREEN_SIZE, flags=SRCALPHA, depth=32 )
    console_area.set_alpha(255)
    console_area.fill( (20,20,20) )
    console_area.blit(cblocals.default_font_big.render("This will be the", True, (255, 255, 255)), (2,0) )
    console_area.blit(cblocals.default_font_big.render("console/command", True, (255, 255, 255)), (2,20) )
    console_area.blit(cblocals.default_font_big.render("area", True, (255, 255, 255)), (2,40) )
    
    charas = level['charas']
    enemies = level['enemies']
    physical = level['physical']
    tippable = level['tippable']
    speech = level['speech']
    while True:
        # ******* EVENTS LOOP BEGIN *******
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit(0)
            
            if event.type==KEYDOWN:
                pressed_keys = pygame.key.get_pressed()

                if not level.presentation and pressed_keys[K_0]:
                    hero.shout("Hey!")

                if level.presentation is not None:
                    if pressed_keys[K_RIGHT]:
                        cblocals.game_speed = cblocals.game_speed*2
                        logging.info("Game speed changed to %s" % cblocals.game_speed)
                    elif pressed_keys[K_LEFT] and cblocals.game_speed>1.:
                        cblocals.game_speed = cblocals.game_speed/2
                        logging.info("Game speed changed to %s" % cblocals.game_speed)

                if pressed_keys[K_F1]:
                    cblocals.FULLSCREEN = not cblocals.FULLSCREEN
                    screen = handleFullScreen()

                if pressed_keys[K_ESCAPE]:
                    if level.presentation is not None:
                        cblocals.game_speed = 128.
                    else:
                        game_over()

            if cblocals.global_controlsEnabled:
                # No mouse control during presentations
                
                if event.type==MOUSEBUTTONDOWN or cblocals.global_leftButtonIsDown:
                    mouse_pos = pygame.mouse.get_pos()
                    if utils.checkPointIsInsideRectType(mouse_pos, ( (0,0),cblocals.GAME_SCREEN_SIZE ) ):
                        logging.debug("Click on %s (%s on level)" % (mouse_pos, level.transformToLevelCoordinate(mouse_pos)))
                        lb, cb, rb = pygame.mouse.get_pressed()
                        if lb and not cblocals.global_leftButtonIsDown:
                            cblocals.global_leftButtonIsDown = True
                        if lb:
                            cblocals.global_lastMouseLeftClickPosition = mouse_pos
                        elif rb:
                            cblocals.global_lastMouseRightClickPosition = mouse_pos
                if event.type==MOUSEBUTTONUP:
                    cblocals.global_leftButtonIsDown = False
    
                if event.type==cblocals.ATTACK_OCCURRED_EVENT:
                    print "Attack from %s" % event.character.name
                    hit_list = charas.rectCollisionWithCharacterHeat(event.character, event.attack.rect)
                    for hit in hit_list:
                        attackRes = event.character.roll_for_hit(hit)
                        if attackRes in module_th0.TH0_ALL_SUCCESSFUL:
                            print "  hit %s" % hit.name
                            hit.generatePhysicalAttackEffect(attack_origin=event.character, criticity=attackRes)
                        else:
                            print "  missed %s" % hit.name

            if event.type==cblocals.SHOUT_EVENT:
                logging.info('%s shouted "%s" from position %s.' % (event.character.name,
                                                              event.text,
                                                              event.position))

            # Sprite collision event
            if event.type==cblocals.SPRITE_COLLISION_EVENT:
                GameSprite.manageCollisions(event.source, event.to)

            # Change current level
            if event.type==cblocals.LEVEL_CHANGE_EVENT:
                exit = event.exit
                level = loadLevelByName(exit.to_level, hero)
                level.topleft = exit.nextTopleft
                level.timeIn=0.
                hero.position = exit.start_position
                hero.navPoint = exit.firstNavPoint
                utils.changeMouseCursor(None)
                charas = level['charas']
                enemies = level['enemies']
                physical = level['physical']
                tippable = level['tippable']
                speech = level['speech']
                break

            # Trigger fired
            if event.type==cblocals.TRIGGER_FIRED_EVENT:
                trigger = event.trigger
                sprite_trigging = event.sprite
                trigger.getResult()
            

        # ******* EVENTS LOOP END *******


        if level.presentation is None or not pygame.key.get_pressed()[K_LCTRL]:
            time_passed = clock.tick() / 1000.  * cblocals.game_speed
            cblocals.game_time = pygame.time.get_ticks()
        else:
            continue
        
        # Level text overlay
        if level.update_text(time_passed):
            level.draw(screen)
            pygame.display.update(pygame.Rect( (0,0), cblocals.GAME_SCREEN_SIZE ))
            continue
        
        # Presentation
        if level.presentation is not None:
            commands = level.presentation.update(time_passed)
            if commands:
                for command in commands:
                    exec command
            elif commands is None:
                logging.info("Presentation: presentation is ended")
                level.presentation = None

        level.update(time_passed)        
        level.draw(screen)
        
        if cblocals.global_controlsEnabled:
            level.normalizeDrawPositionBasedOn(hero, time_passed)
        elif level.screenReferenceSprite:
            level.normalizeDrawPositionBasedOn(level.screenReferenceSprite, time_passed)

        if cblocals.DEBUG:
            physical.drawCollideRect(screen)
            physical.drawMainRect(screen) 
            physical.drawPhysicalRect(screen)
            charas.drawNavPoint(screen)

        charas.drawAttacks(screen, time_passed)

        if cblocals.DEBUG:
            charas.drawHeatRect(screen)

        # points
        if cblocals.globals['points']:
            for displayable in [x for x in charas.sprites() if x.isAlive]:
                displayable.drawPointsInfos(screen)

        # textTips
        if cblocals.globals['text_tips']:
            for displayable in [x for x in tippable.sprites() if x.getTip()]:
                level.displayTip(screen, displayable)

        # Mouse cursor hover an enemy
        # BBB: can I check this in the enemy update method?
        if cblocals.global_controlsEnabled:
            for enemy in enemies.sprites():
                if enemy.physical_rect.collidepoint(pygame.mouse.get_pos()):
                    hero.seeking = enemy
                    utils.changeMouseCursor(cblocals.IMAGE_CURSOR_ATTACK_TYPE)
                    break
            else:
                if cblocals.global_mouseCursorType==cblocals.IMAGE_CURSOR_ATTACK_TYPE:
                    utils.changeMouseCursor(None)
                hero.seeking = None

        if cblocals.global_mouseCursorType:
            utils.drawCursor(screen, pygame.mouse.get_pos())

        # darkness
        if cblocals.SHADOW:
            level.blitShadow(screen, hero)

        # speechs
        speech.draw(screen)

        screen.blit(console_area, (cblocals.GAME_SCREEN_SIZE[0],0) )

        pygame.display.update()


def cheeseBoysInit():
    """Init of the engine"""    
    LOGLEVEL_CHOICES = ('ERROR','WARN','INFO', 'DEBUG')
    DARKNESS_CHOICES = ('on', 'off')
    usage = "usage: %prog [options] [arg]"
    p = optparse.OptionParser(usage=usage, description="Run the Cheese Boys game engine, or execute some other usefull utility instead if you give some of the options below.")
    p.add_option('--version', '-v', action='store_true', help='print software version then exit')
    p.add_option('--debug', '-d', action="store_true", help="Enable game debug mode (for develop and test purpose)")
    p.add_option('--logverbosity', '-l', default="WARN", action="store", choices=LOGLEVEL_CHOICES, help='set the game log verbosity, one of %s (default is ERROR)' % ",".join(LOGLEVEL_CHOICES), metavar="VERBOSITY")
    p.add_option('--tests', '-t', action='store_true', help='run all game unittests') 
    p.add_option('--fullscreen', '-f', action='store_true', help='load the game in fullscreen mode')
    p.add_option('--darkness', '-k', default="on", action="store", choices=DARKNESS_CHOICES, help='valid values are on (default) or off. Act on darkness effect. This can slow down the game engine on less powerfull systems')
    p.add_option("--parse", "-p" , action='store_true', help=("parse a data file for dinamically change the content. See also -cbp options"
                                                              "You can also use the --timestamp option to begin begin operation only after found a specific timestamp"))
    p.add_option("--cbp", "-c" , dest="cbp_filename", help="Must be used in combination of -p option. Parse a .cbp file to change absolute timestamps with dinamical ones. ", metavar="FILE")
    p.add_option("--timestamp", dest="timestamp", help="Use this for other options that can require timestamp values", metavar="TIMESTAMP")

    options, arguments = p.parse_args()
    
    if options.version:
        print "Cheese Boys version %s" % cblocals.__version__
        exit()

    if options.logverbosity=="ERROR":
        logging.getLogger().setLevel(logging.ERROR)
    elif options.logverbosity=="WARN":
        logging.getLogger().setLevel(logging.WARN)
    elif options.logverbosity=="INFO":
        logging.getLogger().setLevel(logging.INFO)
    elif options.logverbosity=="DEBUG":
        logging.getLogger().setLevel(logging.DEBUG)
    else:
        print "error: %s is an invalid option for --logverbosity option, use one of %s" % (options.logverbosity, ",".join(LOGLEVEL_CHOICES))  
        sys.exit(1)

    if options.tests:
        tests()
        exit()

    if options.fullscreen:
        cblocals.FULLSCREEN = True

    if options.darkness=='on':
        cblocals.SHADOW = True
    elif options.darkness=='off':
        cblocals.SHADOW = False

    if options.parse:
        if not options.cbp_filename:
            print "error: The --parse parameter need also the use of --cbp option."
            sys.exit(1)
        else:
            from cheeseboys.presentation.presentation_parser import PresentationParser
            outFile = None
            if arguments:
                outFile = arguments[0]
            PresentationParser.replaceCbpFileAbsoluteTimestamps(options.cbp_filename, options.timestamp, outFile)
            sys.exit(0)

    cblocals.object_registry = UniqueObjectRegistry()

    cblocals.game_time = pygame.time.get_ticks()

    # init of some pygame graphics stuff
    pygame.init()
    screen = handleFullScreen()
    pygame.display.set_icon(utils.load_image("cheese_icon.gif",simpleLoad=True))
    gettext.install('cheeseboys', 'data/i18n', unicode=1)

    if cblocals.SHADOW:
        cblocals.shadow_image = utils.load_image("lightray_1.png", "shadows", simpleLoad=True)
        cblocals.shadow_image.set_alpha(0, RLEACCEL)
        cblocals.total_shadow_image_09 = utils.load_image("total_dark_09.png", "shadows", simpleLoad=True)
        cblocals.total_shadow_image_09.set_alpha(0, RLEACCEL)
        cblocals.total_shadow_image_05 = utils.load_image("total_dark_05.png", "shadows", simpleLoad=True)
        cblocals.total_shadow_image_05.set_alpha(0, RLEACCEL)

    cblocals.default_font = pygame.font.Font("%s/%s" % (cblocals.FONTS_DIR_PATH, cblocals.DEFAULT_FONT), 12)
    cblocals.font_mini = pygame.font.Font("%s/%s" % (cblocals.FONTS_DIR_PATH, cblocals.DEFAULT_FONT), 10)
    cblocals.default_font_big = pygame.font.Font("%s/%s" % (cblocals.FONTS_DIR_PATH, cblocals.DEFAULT_FONT), 16)
    cblocals.speech_font = pygame.font.Font("%s/%s" % (cblocals.FONTS_DIR_PATH, cblocals.DEFAULT_FONT), 14)
    cblocals.leveltext_font = pygame.font.Font("%s/%s" % (cblocals.FONTS_DIR_PATH, cblocals.DEFAULT_LEVELTEXT_FONT), 24)
    cblocals.main_title_font = pygame.font.Font("%s/%s" % (cblocals.FONTS_DIR_PATH, cblocals.MAIN_TITLE_FONT), 72)


def tests():
    import unittest
    from cheeseboys import tests as cbtests
    unittest.TextTestRunner(verbosity=2).run(cbtests.test_presentation.alltests)


def menu():
    """Main menu"""
    pygame.display.set_caption("Cheese Boys (alpha release) %s" % cblocals.__version__)
    # Init game menu
    screen = cblocals.screen
    menu = kezmenu.KezMenu(
        [_(u"Start Game"), game],
        [_(u"Check for new version"), lambda: utils.update_version(screen, pygame.Rect( (50,230),(350,300) ) )],
        [_(u"Quit"), game_over],
        )
    menu.set_font(cblocals.leveltext_font)    
    image = utils.load_image('cheese-boys-logo.png')
    
    menu.center_at(600, 300)
    menu.set_normal_color( (255,255,255) )
    to_display = u'Cheese Boys'
    to_display_size = cblocals.main_title_font.size(to_display)
    title_text = cblocals.main_title_font.render(to_display, True, (252,252,112))
    text_start_pos_x, text_start_pos_y = (cblocals.SCREEN_SIZE[0]/2-to_display_size[0]/2, 100)

    while True:
        events = pygame.event.get()
        menu.update(events)

        for e in events:
            if e.type == pygame.QUIT:
                game_over()

        screen.fill((0, 0, 0))
        screen.blit(image, (text_start_pos_x-20-image.get_width(),text_start_pos_y) )
        screen.blit(title_text, (text_start_pos_x,text_start_pos_y) )
        menu.draw(screen)
        pygame.display.flip()

def game_over():
    """end python, but pygame first"""
    pygame.quit()
    print _("Game Over")
    sys.exit(0)

if __name__ == "__main__":
    cheeseBoysInit()
    menu()
    
    
