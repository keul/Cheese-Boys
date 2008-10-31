# -*- coding: utf-8 -

from cheeseboys.level import GameLevel
from cheeseboys.pygame_extensions import GameGroup
from cheeseboys import character
from cheeseboys.level import GameLevel
from cheeseboys.ai.base_brain import BaseStateMachine
from cheeseboys.sprites import CodigoroSign, LevelExit, Gate

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

    boss = character.Character("The Boss", ("enemy2_sword.png","enemy2.png"), (all,charas,enemies,physical), realSize=(18,25), speed=140., weaponInAndOut=True)
    boss.setBrain(BaseStateMachine)
    boss.setCombatValues(2, 10)
    boss.hitPoints = boss.hitPointsLeft = 25

    level.addSprite(hero, hero.position)
    level.addSprite(boss, (740, 320))

    level.addPhysicalBackground( (1000,700), (800, 250) )
    level.addPhysicalBackground( (136,318), (273, 118) )
    level.addPhysicalBackground( (487,375), (430, 180) )
    level.addPhysicalBackground( (300,700), (600, 380) )
    level.addPhysicalBackground( (146,40), (127, 40) )
    level.addPhysicalBackground( (349,40), (114, 40) )
    level.addPhysicalBackground( (41,38), (83, 39) )

    exits1 = LevelExit( (1382,452), (36,410), "The South Bridge", (-200, 100), (100,150), (0, 0), exits)
    level.addSprite(exits1, (1382,452) )
    exits2 = LevelExit( (249,28), (84,30), None, None, None, None, exits)
    level.addSprite(exits2, (249,28) )
    exits3 = LevelExit( (618,452), (36,76), None, None, None, None, exits)
    level.addSprite(exits3, (618,452) )
    exits4 = LevelExit( (15,200), (30,162), None, None, None, None, exits)
    level.addSprite(exits4, (15,200) )

    gate1 = Gate( (80,200), 162, 1, physical)
    level.addSprite(gate1)
    gate2 = Gate( (690,452), 74, 1, physical)
    level.addSprite(gate2)
    

    level.enableRainEffect()
    
    return level