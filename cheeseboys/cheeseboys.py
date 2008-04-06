# -*- coding: utf-8 -*-

import sys

import pygame
from pygame.locals import *

import character
import locals

def main():
    pygame.init()
    clock = pygame.time.Clock()
    
    screen = pygame.display.set_mode( (locals.SCREEN_WIDTH, locals.SCREEN_HEIGHT), 0, 32)
    pygame.display.set_caption("CheeseBoys")
    #pygame.key.set_repeat(0, 0)
    
    background = pygame.Surface( (640, 480), flags=SRCALPHA, depth=32 )
    all = pygame.sprite.RenderUpdates()
    hero = character.Character("Luca", "hero", (all,))
    
    direction = locals.DIRECTION_E
    
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
        #screen.blit(hero.sprite, hero.position)

        all.draw(screen)
                
        pygame.display.update()



if __name__ == "__main__":
    main()
