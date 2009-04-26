# -*- coding: utf-8 -

import pygame
from cheeseboys import cblocals

def loadAnimationByName(name, position, *containers):
    """Try to load an animation sprite know to the application.
    This method know how big is the animation size.
    """
    if name=='water-wave':
        from cheeseboys.sprites import WaterWave
        return WaterWave(position, (120,80), *containers)
    if name=='thunders':
        from cheeseboys.sprites import Thunders
        return Thunders(position, cblocals.GAME_SCREEN_SIZE, *containers)
    if name=='lighting':
        from cheeseboys.sprites import Lighting
        return Lighting(position, (103, 652), *containers)
    if name=='dark-largestain':
        from cheeseboys.sprites import DarkLargeStain
        x,y = position
        return DarkLargeStain((x, y+21), (62, 42), *containers)
    else:
        raise ValueError("Value %s is not a know animation." % name)


def show_fps(screen, fps):
    """Display the frame per seconds value on the screen bottom right corner"""
    fps = "FPS: %0d" % fps
    to_display_size = cblocals.font_mini.size(fps)
    to_diplay = cblocals.font_mini.render(fps, True, (255,255,255))
    w,h = cblocals.GAME_SCREEN_SIZE
    screen.blit(to_diplay, (w+5, h-to_display_size[1]-5) )


