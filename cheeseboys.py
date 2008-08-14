# -*- coding: utf-8 -*-

import sys, logging

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
    from cheeseboys.utils import Vector2
except ImportError:
    print ("Vector2 class of gameobjects not found.\n"
           "Please download it from:\n"
           "http://code.google.com/p/gameobjects/")
    sys.exit(1)
print "All required libraries are present!"
# #######

from pygame.locals import *

from cheeseboys import cblocals, utils, character
from cheeseboys.level import GameLevel
from cheeseboys.ai.base_brain import BaseStateMachine
from cheeseboys.ai.hero import HeroStateMachine
from cheeseboys.pygame_extensions import GameGroup

def main():
    clock = pygame.time.Clock()
    
    screen = pygame.display.set_mode( cblocals.SCREEN_SIZE, 0, 32)
    pygame.display.set_caption("Cheese Boys - pre-alpha version %s" % cblocals.__version__)
    
    all = GameGroup("all")
    dead = GameGroup("dead", updatable=True)
    physical = GameGroup("physical", updatable=True)
    charas = GameGroup("charas")
    enemies = GameGroup("enemies")

    hero = character.PlayingCharacter("Luca", ("hero_sword1_vest1.png","hero_vest1.png"), (all,charas,physical), realSize=(18,25), weaponInAndOut=True)
    hero.setBrain(HeroStateMachine)
    hero.setCombatValues(2, 13)
    
    enemy1 = character.Character("Max", ("enemy1_sword.png","enemy1.png"), (all,charas,enemies,physical), realSize=(18,25), speed=100., weaponInAndOut=True)
    enemy1.setBrain(BaseStateMachine)
    enemy1.setCombatValues(0, 5)
    enemy2 = character.Character("John", ("enemy1_sword.png","enemy1.png"), (all,charas,enemies,physical), realSize=(18,25), speed=80., weaponInAndOut=True)
    enemy2.setBrain(BaseStateMachine)
    enemy2.setCombatValues(0, 5)
    enemy3 = character.Character("Jack", ("enemy1_sword.png","enemy1.png"), (all,charas,enemies,physical), realSize=(18,25), speed=125., weaponInAndOut=True)
    enemy3.setBrain(BaseStateMachine)
    enemy3.setCombatValues(0, 5)
    enemy4 = character.Character("Roger", ("enemy1_sword.png","enemy1.png"), (all,charas,enemies,physical), realSize=(18,25), speed=160., weaponInAndOut=True)
    enemy4.setBrain(BaseStateMachine)
    enemy4.setCombatValues(0, 5)

    testLevel = GameLevel("The South Bridge", (800, 1500))
    testLevel.topleft = (100, 900)
    
    testLevel.addSprite(hero, (350, 1450))
    testLevel.addSprite(enemy1, (600, 790))
    testLevel.addSprite(enemy2, (400, 300))
    testLevel.addSprite(enemy3, (320, 210))
    testLevel.addSprite(enemy4, (250, 520))
    testLevel.group_charas = charas

    testLevel.addGroup(dead, zindex=5)
    testLevel.addGroup(physical, zindex=10)
    testLevel.addGroup(charas, zindex=10)

    testLevel.addPhysicalBackground( (0,208), (235, 1130) )
    testLevel.addPhysicalBackground( (487,208), (310, 1130) )    

    console_area = pygame.Surface( cblocals.CONSOLE_SCREEN_SIZE, flags=SRCALPHA, depth=32 )
    
    while True:
        for event in pygame.event.get():
            #print event, event.type
            if event.type == QUIT:
                sys.exit()
            
            if event.type==KEYDOWN:
                pressed_keys = pygame.key.get_pressed()
                
                if pressed_keys[K_ESCAPE]:
                    sys.exit()

            if event.type==MOUSEBUTTONDOWN or cblocals.global_leftButtonIsDown:
                logging.debug("Click on %s,%s" % pygame.mouse.get_pos())
                lb, cb, rb = pygame.mouse.get_pressed()
                if lb and not cblocals.global_leftButtonIsDown:
                    cblocals.global_leftButtonIsDown = True
                if lb:
                    cblocals.global_lastMouseLeftClickPosition = pygame.mouse.get_pos()
                elif rb:
                    cblocals.global_lastMouseRightClickPosition = pygame.mouse.get_pos()
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

        time_passed = clock.tick() / 1000.
        testLevel.update(time_passed)
        
        testLevel.draw(screen)
        testLevel.normalizeDrawPositionBasedOn(hero, time_passed)

        #charas.drawCollideRect(screen)
        #charas.drawMainRect(screen) 
        #charas.drawPhysicalRect(screen)
        #charas.drawNavPoint(screen)

        charas.drawAttacks(screen, time_passed)

        #charas.drawHeatRect(screen)

        # points
        for displayable in [x for x in charas.sprites() if x.isAlive]:
            displayable.drawPointsInfos(screen)

        # textTips
        for displayable in [x for x in charas.sprites() if x.getTip()]:
            screen.blit(displayable.getTip(), displayable.topleft(y=-5) )

        # mouse cursor hover on enemy
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

        screen.blit(console_area, (cblocals.GAME_SCREEN_SIZE[0],0) )
        console_area.blit(cblocals.default_font_big.render("This will be the", True, (255, 255, 255)), (2,0) )
        console_area.blit(cblocals.default_font_big.render("console/command area", True, (255, 255, 255)), (2,30) )

        pygame.display.update()

def cheeseBoysInit():
    """Init of this game engine"""
    logging.getLogger().setLevel(logging.DEBUG)
    cblocals.default_font = pygame.font.SysFont("%s/%s" % (cblocals.FONTS_DIR_PATH, cblocals.DEFAULT_FONT), 16)
    cblocals.default_font_big = pygame.font.SysFont("%s/%s" % (cblocals.FONTS_DIR_PATH, cblocals.DEFAULT_FONT), 20)


if __name__ == "__main__":
    pygame.init()
    cheeseBoysInit()
    main()

