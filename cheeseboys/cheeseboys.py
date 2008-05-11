# -*- coding: utf-8 -*-

import sys

import pygame
from pygame.locals import *

import character
from group import Group
import locals

def main():
    clock = pygame.time.Clock()
    
    screen = pygame.display.set_mode( (locals.SCREEN_WIDTH, locals.SCREEN_HEIGHT), 0, 32)
    locals.screen = screen
    pygame.display.set_caption("CheeseBoys - pre-alpha version %s" % locals.__version__)
    background = pygame.Surface( (640, 480), flags=SRCALPHA, depth=32 )
    
    all = pygame.sprite.RenderUpdates()
    charas = Group()

    hero = character.PlayingCharacter("Luca", ("hero_sword1_vest1.png","hero_vest1.png"), (all,charas), firstPos=(100, 100), realSize=(18,25), weaponInAndOut=True)
    
    enemy1 = character.Character("Max", "enemy1_sword.png", (all,charas), firstPos=(200, 90), realSize=(18,25), speed=100.)
    enemy2 = character.Character("John", "enemy1_sword.png", (all,charas), firstPos=(400, 300), realSize=(18,25), speed=80. )
    enemy3 = character.Character("Jack", "enemy1_sword.png", (all,charas), firstPos=(320, 210), realSize=(18,25), speed=125. )
    enemy4 = character.Character("Roger", "enemy1_sword.png", (all,charas), firstPos=(50, 420), realSize=(18,25), speed=180. )
    
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
                    locals.global_lastMouseLeftClickPosition = pygame.mouse.get_pos()
                elif rb:
                    locals.global_lastMouseRightClickPosition = pygame.mouse.get_pos()

            if event.type==locals.ATTACK_OCCURRED_EVENT:
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

def initFont():
    locals.default_font = pygame.font.SysFont("data/%s" % locals.DEFAULT_FONT, 16)

if __name__ == "__main__":
    pygame.init()
    initFont()
    main()
    test2()

