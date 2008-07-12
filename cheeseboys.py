# -*- coding: utf-8 -*-

import sys

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

from cheeseboys import cblocals, utils
from cheeseboys import character
from cheeseboys.level import GameLevel
from cheeseboys.ai.base_brain import BaseStateMachine
from cheeseboys.ai.hero import HeroStateMachine
from cheeseboys.pygame_extensions import Group

def main():
    clock = pygame.time.Clock()
    
    screen = pygame.display.set_mode( cblocals.SCREEN_SIZE, 0, 32)
    #cblocals.screen = screen
    pygame.display.set_caption("Cheese Boys - pre-alpha version %s" % cblocals.__version__)
    
    all = pygame.sprite.RenderUpdates()
    dead = Group()
    charas = Group()
    enemies = Group()

    hero = character.PlayingCharacter("Luca", ("hero_sword1_vest1.png","hero_vest1.png"), (all,charas), realSize=(18,25), weaponInAndOut=True)
    hero.setBrain(HeroStateMachine)
    
    enemy1 = character.Character("Max", ("enemy1_sword.png","enemy1.png"), (all,charas,enemies), realSize=(18,25), speed=100., weaponInAndOut=True)
    enemy1.setBrain(BaseStateMachine)
    enemy2 = character.Character("John", ("enemy1_sword.png","enemy1.png"), (all,charas,enemies), realSize=(18,25), speed=80., weaponInAndOut=True)
    enemy2.setBrain(BaseStateMachine)
    enemy3 = character.Character("Jack", ("enemy1_sword.png","enemy1.png"), (all,charas,enemies), realSize=(18,25), speed=125., weaponInAndOut=True)
    enemy3.setBrain(BaseStateMachine)
#    enemy4 = character.Character("Roger", ("enemy1_sword.png","enemy1.png"), (all,charas,enemies), realSize=(18,25), speed=180., weaponInAndOut=True)
#    enemy4.setBrain(BaseStateMachine)
    
    testLevel = GameLevel("South bridge", (650, 1200))
    testLevel.topleft = (0, 600)
    testLevel.group_dead = dead
    
    testLevel.addSprite(hero, (100, 1100))
    testLevel.addSprite(enemy1, (600, 790))
    testLevel.addSprite(enemy2, (400, 300))
    testLevel.addSprite(enemy3, (320, 210))
#    testLevel.addSprite(enemy4, (50, 420))
    testLevel.group_charas = charas

    background = pygame.Surface( cblocals.GAME_SCREEN_SIZE, flags=SRCALPHA, depth=32 )
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
                    print "  hit %s" % hit.name
                    hit.generatePhysicalAttachEffect(attack_origin=event.character)

        time_passed = clock.tick() / 1000.
        all.update(time_passed)
        
        screen.blit(background, (0,0) )
        testLevel.draw(screen)
        testLevel.normalizeDrawPositionBasedOn(hero, time_passed)

        #charas.drawCollideRect(screen)
        #charas.drawMainRect(screen) 
        #charas.drawPhysicalRect(screen)
        #charas.drawNavPoint(screen)

        dead.draw(screen)

        all.draw(screen)
        charas.drawAttacks(screen, time_passed)

        #charas.drawHeatRect(screen)

        # points
        for displayable in [x for x in charas.sprites() if x.isAlive]:
            displayable.drawPointsInfos(screen)

        # textTips
        for displayable in [x for x in all.sprites() if x.getTip()]:
            screen.blit(displayable.getTip(), displayable.topleft(y=-5) )

        # mouse cursor
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
    cblocals.default_font = pygame.font.SysFont("%s/%s" % (cblocals.FONTS_DIR_PATH, cblocals.DEFAULT_FONT), 16)
    cblocals.default_font_big = pygame.font.SysFont("%s/%s" % (cblocals.FONTS_DIR_PATH, cblocals.DEFAULT_FONT), 20)


if __name__ == "__main__":
    pygame.init()
    cheeseBoysInit()
    main()

