# -*- coding: utf-8 -*-

import sys

import pygame
from pygame.locals import *

from cheeseboys import cblocals
from cheeseboys import character
from cheeseboys.level import GameLevel
from cheeseboys.ai.ferrarese import FerrareseStateMachine
from cheeseboys.pygame_extensions import Group

def main():
    clock = pygame.time.Clock()
    
    screen = pygame.display.set_mode( cblocals.SCREEN_SIZE, 0, 32)
    #cblocals.screen = screen
    pygame.display.set_caption("Cheese Boys - pre-alpha version %s" % cblocals.__version__)
    background = pygame.Surface( cblocals.SCREEN_SIZE, flags=SRCALPHA, depth=32 )
    
    all = pygame.sprite.RenderUpdates()
    charas = Group()

    hero = character.PlayingCharacter("Luca", ("hero_sword1_vest1.png","hero_vest1.png"), (all,charas), realSize=(18,25), weaponInAndOut=True)
    
    enemy1 = character.Character("Max", ("enemy1_sword.png","enemy1.png"), (all,charas), realSize=(18,25), speed=100., weaponInAndOut=True)
    enemy1.setBrain(FerrareseStateMachine)
    enemy2 = character.Character("John", ("enemy1_sword.png","enemy1.png"), (all,charas), realSize=(18,25), speed=80., weaponInAndOut=True)
    enemy2.setBrain(FerrareseStateMachine)
    enemy3 = character.Character("Jack", ("enemy1_sword.png","enemy1.png"), (all,charas), realSize=(18,25), speed=125., weaponInAndOut=True)
    enemy3.setBrain(FerrareseStateMachine)
    enemy4 = character.Character("Roger", ("enemy1_sword.png","enemy1.png"), (all,charas), realSize=(18,25), speed=180., weaponInAndOut=True)
    enemy4.setBrain(FerrareseStateMachine)
    
    testLevel = GameLevel("South bridge", cblocals.SCREEN_SIZE)
    testLevel.addCharacter(hero, (100, 100))
    testLevel.addCharacter(enemy1, (200, 90))
    testLevel.addCharacter(enemy2, (400, 300))
    testLevel.addCharacter(enemy3, (320, 210))
    testLevel.addCharacter(enemy4, (50, 420))
    testLevel.charasGroup = charas
    
    while True:
        for event in pygame.event.get():
            #print event, event.type
            if event.type == QUIT:
                sys.exit()
            
            if event.type==KEYUP:
                hero.moving(False)
            
            if event.type==KEYDOWN:
                pressed_keys = pygame.key.get_pressed()
                
                if pressed_keys[K_ESCAPE]:
                    sys.exit()
    
            if event.type==MOUSEBUTTONDOWN:
                lb, cb, rb = pygame.mouse.get_pressed()
                if lb:
                    cblocals.global_lastMouseLeftClickPosition = pygame.mouse.get_pos()
                elif rb:
                    cblocals.global_lastMouseRightClickPosition = pygame.mouse.get_pos()

            if event.type==cblocals.ATTACK_OCCURRED_EVENT:
                print "Attack from %s" % event.character.name
                hit_list = charas.rectCollisionWithCharacterHeat(event.character, event.attack.rect)
                for hit in hit_list:
                    print "  hit %s" % hit.name

        time_passed = clock.tick() / 1000.
        all.update(time_passed)
        
        screen.blit(background, (0,0) )
        
#        charas.drawCollideRect(screen)
#        charas.drawMainRect(screen) 
#        charas.drawPhysicalRect(screen)

        all.draw(screen)
        charas.drawAttacks(screen, time_passed)

#        charas.drawHeatRect(screen)

        #textTips
        for displayable in [x for x in all.sprites() if x.getTip()]:
            screen.blit(displayable.getTip(), displayable.topleft(y=-5) )

        pygame.display.update()

def cheeseBoysInit():
    cblocals.default_font = pygame.font.SysFont("%s/%s" % (cblocals.FONTS_DIR_PATH, cblocals.DEFAULT_FONT), 16)

if __name__ == "__main__":
    pygame.init()
    cheeseBoysInit()
    main()

