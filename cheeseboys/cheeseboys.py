# -*- coding: utf-8 -*-

import sys

import pygame
from pygame.locals import *

import character
import locals

def main():
    clock = pygame.time.Clock()
    
    screen = pygame.display.set_mode( (locals.SCREEN_WIDTH, locals.SCREEN_HEIGHT), 0, 32)
    locals.screen = screen
    pygame.display.set_caption("CheeseBoys")
    #pygame.key.set_repeat(0, 0)
    
    background = pygame.Surface( (640, 480), flags=SRCALPHA, depth=32 )
    all = pygame.sprite.RenderUpdates()
    hero = character.PlayingCharacter("Luca", "hero", (all,))
    
    enemy1 = character.Character("Max", "hero", (all,), firstPos=(200, 90), speed=180.)
    enemy2 = character.Character("John", "hero", (all,), firstPos=(400, 300), speed=60. )
    enemy3 = character.Character("Jack", "hero", (all,), firstPos=(320, 210), speed=125. )
    enemy4 = character.Character("Roger", "hero", (all,), firstPos=(50, 420), speed=200. )
    
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
                locals.global_lastMouseLeftClickPosition = pygame.mouse.get_pos()

        time_passed = clock.tick() / 1000.
        all.update(time_passed)
        
        screen.blit(background, (0,0) )

        all.draw(screen)

        #textTips
        for displayable in [x for x in all.sprites() if x.getTip()]:
            screen.blit(displayable.getTip(), displayable.topleft(y=-10) )

        pygame.display.update()

def initFont():
    locals.default_font = pygame.font.SysFont("data/%s" % locals.DEFAULT_FONT, 16)

if __name__ == "__main__":
    pygame.init()
    initFont()
    main()
