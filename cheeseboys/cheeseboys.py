# -*- coding: utf-8 -*-

import sys

import pygame
from pygame.locals import *

import character
import locals

#from cursor import CursorHandler

def main():
    clock = pygame.time.Clock()
    
    screen = pygame.display.set_mode( (locals.SCREEN_WIDTH, locals.SCREEN_HEIGHT), 0, 32)
    locals.screen = screen
    #locals.cursorHandler = CursorHandler()
    pygame.display.set_caption("CheeseBoys - pre-alpha")
    #pygame.key.set_repeat(0, 0)
    
    background = pygame.Surface( (640, 480), flags=SRCALPHA, depth=32 )
    all = pygame.sprite.RenderUpdates()
    hero = character.PlayingCharacter("Luca", "hero_sword1_vest1.png", (all,))
    
    enemy1 = character.Character("Max", "enemy1_sword.png", (all,), firstPos=(200, 90), speed=180.)
    enemy2 = character.Character("John", "enemy1_sword.png", (all,), firstPos=(400, 300), speed=60. )
    enemy3 = character.Character("Jack", "enemy1_sword.png", (all,), firstPos=(320, 210), speed=125. )
    enemy4 = character.Character("Roger", "enemy1_sword.png", (all,), firstPos=(50, 420), speed=200. )
    
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

def test():
    s = pygame.image.load("data/images/charas/enemy1_sword.png")
    screen = pygame.display.set_mode( (locals.SCREEN_WIDTH, locals.SCREEN_HEIGHT), 0, 32)
    
    s2 = s.subsurface( (48,64), (24,32) )
    screen.blit(s2, (0,0) )
    
    c = 0
    import utils
    for x in utils.load_image("hero_sword1_vest1.png", "charas", charasFormatImage=True):
        c+=1
        screen.blit(x, (c*34,70) )
    
    pygame.display.update()
    
    while True:
        for event in pygame.event.get():
            #print event, event.type
            if event.type == QUIT:
                sys.exit()

if __name__ == "__main__":
    pygame.init()
    initFont()
    main()
    #test()

