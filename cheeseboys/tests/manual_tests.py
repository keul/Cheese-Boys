# -*- coding: utf-8 -

def test():
    from math import *
    from utils import Vector2
    screen = pygame.display.set_mode( (locals.SCREEN_WIDTH, locals.SCREEN_HEIGHT), 0, 32)
    bk = pygame.image.load("/home/keul/immagini/1993-Mazda-RX-7-Twin-Turbo-Mk-III-Factory-Photos-F-640.jpeg").convert()
    
    s2 = pygame.Surface( (250,250), flags=SRCALPHA, depth=32 ).convert_alpha()
    pygame.draw.rect(s2, (0,0,0), (0,0,249,249), 1 )
    
    rotation = 0.
    rotation_direction = 0.
    movement_direction = 0.
    rotation_speed = 120.
    
    clock = pygame.time.Clock()
    
    x=120
    y=100
    
    while True:
        time_passed = clock.tick() / 1000.
        rotation_direction=0
        for event in pygame.event.get():
            #print event, event.type
            if event.type == QUIT:
                sys.exit()
            
            pressed_keys = pygame.key.get_pressed()
            if pressed_keys[K_LEFT]:
                rotation_direction=-1.
            if pressed_keys[K_RIGHT]:
                rotation_direction=1.

        screen.blit(bk, (0,0))
        s2.fill( (127,127,127,10,) )
        pygame.draw.circle(s2, (0,0,0,180), (x,y) , 5)
        pygame.draw.line(s2, (120,120,120,200), (120,240), (x, y), 2 )
        screen.blit(s2, (120,120) )
        pygame.display.update()

        rotation += rotation_direction * rotation_speed * time_passed
        print "rot:", rotation
        
        hx = sin(rotation*pi*180.0)
        hy = cos(rotation*pi*180.0)
        #h = Vector2(hx, hy)
        #h*=movement_direction
        #x,y = h*time_passed
        x+=hx;y+=hy
        print "x,y", x, y

def test2():
    from math import pi
    screen = pygame.display.set_mode( (locals.SCREEN_WIDTH, locals.SCREEN_HEIGHT), 0, 32)
    bk = pygame.image.load("/home/keul/immagini/1993-Mazda-RX-7-Twin-Turbo-Mk-III-Factory-Photos-F-640.jpeg").convert()
    
    s2 = pygame.Surface( (250,250), flags=SRCALPHA, depth=32 ).convert_alpha()
    s2.fill( (127,127,127,10,) )
    #s3 = pygame.Surface( (250,250), flags=SRCALPHA, depth=32 ).convert_alpha()
    er = (0,0,50,50)
    
    deg1 = 0
    deg2 = 20
    
    pygame.draw.rect(s2, (0,0,0), (0,0,249,249), 1 )
    pygame.draw.rect(s2, (0,0,0), er, 1 )
    pygame.draw.arc(s2, (0,0,0,120), er, deg1*pi*180.0, deg2*pi*180.0, 5  )
    #pygame.draw.ellipse(s3, (127,127,127,120) , (10,10,200,150), 3)
    
    screen.blit(bk, (0,0))
    screen.blit(s2, (10,10) )
    #screen.blit(s3, (300,300) )
    
    pygame.display.update()
    
    while True:
        for event in pygame.event.get():
            #print event, event.type
            if event.type == QUIT:
                sys.exit()