#! /usr/bin/python
# -*- coding: utf-8 -*-

import sys, logging, optparse
import gettext

# CHECKING GAME DEPENDENCIES
print "Checking dependencies..."
try:
    import pygame
except ImportError:
    print ("Pygame module isn't present!\n"
           "This is the main game module! You must download it from\n"
           "http://pygame.org/download.shtml")
    sys.exit(1)
try:
    from gameobjects.vector2 import Vector2
except ImportError:
    print ("Vector2 class of gameobjects not found.\n"
           "I'll use a local version of the library.\n"
           "Please consider to download Will McGugan's original code from:\n"
           "http://code.google.com/p/gameobjects/")
print "All required libraries are present."
# #######

from pygame.locals import *

from cheeseboys import cblocals, utils, character
from cheeseboys.level import loadLevelByName
from cheeseboys.ai.hero import HeroStateMachine

def main():
    
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(cblocals.SCREEN_SIZE, 0, 32)

    hero = character.PlayingCharacter("Luca", ("hero_sword1_vest1.png","hero_vest1.png"), (), realSize=(18,25), weaponInAndOut=True)
    hero.setBrain(HeroStateMachine)
    hero.setCombatValues(2, 13)

    level = loadLevelByName("The South Bridge", hero)
    level.enablePresentation('funny-intro')
    
    pygame.display.set_caption("Cheese Boys (alpha release) %s - %s" % (cblocals.__version__, level.name))

    console_area = pygame.Surface( cblocals.CONSOLE_SCREEN_SIZE, flags=SRCALPHA, depth=32 )
    console_area.set_alpha(255)
    
    charas = level['charas']
    enemies = level['enemies']
    while True:
        for event in pygame.event.get():
            #print event, event.type
            if event.type == QUIT:
                sys.exit()
            
            if event.type==KEYDOWN:
                pressed_keys = pygame.key.get_pressed()
                
                if pressed_keys[K_ESCAPE]:
                    sys.exit()

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
                        if attackRes==cblocals.TH0_HIT or attackRes==cblocals.TH0_HIT_CRITICAL:
                            print "  hit %s" % hit.name
                            hit.generatePhysicalAttachEffect(attack_origin=event.character, criticity=attackRes)
                        else:
                            print "  missed %s" % hit.name

            if event.type==cblocals.SHOUT_EVENT:
                logging.info('%s shouted "%s" from position %s.' % (event.character.name,
                                                              event.text,
                                                              event.position))

        if level.presentation is None or not pygame.key.get_pressed()[K_LCTRL]:
            time_passed = clock.tick() / 1000.
        else:
            continue

        if level.update_text(time_passed):
            level.draw(screen)
            continue

        level.update(time_passed)
        
        if level.presentation:
            command = level.presentation.update(time_passed)
            if command:
                exec command
            if command is None:
                level.presentation = None
        
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
            for displayable in [x for x in charas.sprites() if x.getTip()]:
                screen.blit(displayable.getTip(), displayable.topleft(y=-5) )

        # mouse cursor hover on enemy
        if cblocals.global_controlsEnabled:
            for enemy in enemies.sprites():
                if enemy.physical_rect.collidepoint(pygame.mouse.get_pos()):
                    hero.seeking = enemy
                    utils.changeMouseCursor(cblocals.IMAGE_CURSOR_ATTACK_TYPE)
                    utils.drawCursor(screen, pygame.mouse.get_pos())
                    break
            else:
                if cblocals.global_mouseCursor is not None:
                    utils.changeMouseCursor(None)
                hero.seeking = None

        level.drawRain(screen, time_passed)

        screen.blit(console_area, (cblocals.GAME_SCREEN_SIZE[0],0) )
        console_area.blit(cblocals.default_font_big.render("This will be the", True, (255, 255, 255)), (2,0) )
        console_area.blit(cblocals.default_font_big.render("console/command area", True, (255, 255, 255)), (2,30) )

        pygame.display.update()

def cheeseBoysInit():
    """Init of this game engine"""
    
    gettext.install('cheeseboys', 'data/i18n', unicode=1)
    
    LOGLEVEL_CHOICES = ('ERROR','WARN','INFO', 'DEBUG')
    p = optparse.OptionParser( )
    p.add_option('--version', '-v', action='store_true', help='print software version then exit')
    p.add_option('--debug', '-d', action="store_true", help="Enable game debug mode (for develop and test purpose)")
    p.add_option('--logverbosity', '-l', default="WARN", action="store", choices=LOGLEVEL_CHOICES, help='set the game log verbosity, one of %s (default is ERROR)' % ",".join(LOGLEVEL_CHOICES))
    p.add_option('--tests', '-t', action='store_true', help='run all game unittests') 

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
        print "%s is an invalid option for --logverbosity option, use one of %s" % (options.logverbosity, ",".join(LOGLEVEL_CHOICES))  

    if options.tests:
        tests()
        exit()

    cblocals.default_font = pygame.font.SysFont("%s/%s" % (cblocals.FONTS_DIR_PATH, cblocals.DEFAULT_FONT), 16)
    cblocals.default_font_big = pygame.font.SysFont("%s/%s" % (cblocals.FONTS_DIR_PATH, cblocals.DEFAULT_FONT), 20)
    cblocals.speech_font = pygame.font.SysFont("%s/%s" % (cblocals.FONTS_DIR_PATH, cblocals.DEFAULT_FONT), 14)
    cblocals.leveltext_font = pygame.font.SysFont("%s/%s" % (cblocals.FONTS_DIR_PATH, cblocals.DEFAULT_LEVELTEXT_FONT), 26)

def tests():
    import unittest
    from cheeseboys import tests as cbtests
    unittest.TextTestRunner(verbosity=2).run(cbtests.test_presentation.alltests)


if __name__ == "__main__":
    pygame.init()
    cheeseBoysInit()
    main()
    
    
