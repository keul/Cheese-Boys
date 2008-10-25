# -*- coding: utf-8 -

from cheeseboys.level import GameLevel
from cheeseboys.pygame_extensions import GameGroup
from cheeseboys import character
from cheeseboys.level import GameLevel
from cheeseboys.ai.base_brain import BaseStateMachine
from cheeseboys.sprites import CodigoroSign, LevelExit

def load(name, hero):
    level = GameLevel(_(str(name)), (1400, 700))
    level.hero = hero

    all = level['all']
    charas = level['charas']
    enemies = level['enemies']
    physical = level['physical']
    exits = level['exits']
    animations = level['animations']
    hero.addToGroups(all, charas, physical)

    # TODO



    level.enableRainEffect()
    
    return level