# -*- coding: utf-8 -

from cheeseboys.level import GameLevel
from cheeseboys import character
from cheeseboys.level import GameLevel
from cheeseboys.ai.base_brain import BaseStateMachine
from cheeseboys.sprites import CodigoroSign, LevelExit, Gate
from cheeseboys.sprites.triggers import PresentationTrigger

def load(name, hero):
    level = GameLevel(_(str(name)), (1400, 700))
    level.hero = hero

    all = level['all']
    charas = level['charas']
    enemies = level['enemies']
    physical = level['physical']
    exits = level['exits']
    animations = level['animations']
    triggers = level['triggers']
    hero.addToGroups(all, charas, physical)

    boss = character.Character("The Boss", ("enemy2_sword.png","enemy2.png"), (all,charas,enemies,physical), realSize=(18,25), speed=140., weaponInAndOut=True)
    boss.setBrain(BaseStateMachine)
    boss.brain_enabled=False
    boss.setCombatValues(2, 10)
    boss.attackDamage = "1d8"
    boss.hitPoints = boss.hitPointsLeft = 25
    boss.rest_time_needed = .25
    
    enemy1 = character.Character("Phil", ("enemy1_sword.png","enemy1.png"), (all,charas,enemies,physical), realSize=(18,25), speed=130., weaponInAndOut=True)
    enemy1.setBrain(BaseStateMachine)
    enemy1.brain_enabled=False
    enemy1.setCombatValues(2, 6)

    level.addSprite(hero, hero.position)
    level.addSprite(boss, (740, 320))
    level.addSprite(enemy1, (750, 360))

    level.addPhysicalBackground( (1000,700), (800, 250) )
    level.addPhysicalBackground( (136,318), (273, 118) )
    level.addPhysicalBackground( (487,375), (430, 180) )
    level.addPhysicalBackground( (300,700), (600, 380) )
    level.addPhysicalBackground( (146,40), (127, 40) )
    level.addPhysicalBackground( (349,40), (114, 40) )
    level.addPhysicalBackground( (41,38), (83, 39) )

    level.addAnimations(((695,536),(863,622),(993,530),(1262,507),), 'water-wave')

    exits1 = LevelExit( (1382,452), (36,410), "The South Bridge", (-200, 100), (100,150), (0, 0), exits)
    level.addSprite(exits1, (1382,452) )
    exits2 = LevelExit( (249,28), (84,30), None, None, None, None, exits)
    level.addSprite(exits2, (249,28) )
    exits3 = LevelExit( (618,452), (36,76), None, None, None, None, exits)
    level.addSprite(exits3, (618,452) )
    exits4 = LevelExit( (15,200), (30,162), None, None, None, None, exits)
    level.addSprite(exits4, (15,200) )

    gate1 = Gate( (80,200), 162, 1, physical)
    gate1.name = "Exit"
    gate1.open_condition = (boss, 'isAlive')
    gate1.open_condition_reverse_flag = True
    level.addSprite(gate1)
    gate2 = Gate( (690,452), 74, 1, physical)
    level.addSprite(gate2)
    gate3 = Gate( (251,75), 84, 0, physical)
    level.addSprite(gate3)
    
    triggerPresentation = PresentationTrigger( (1170,452), (20,452), (hero,), triggers )
    triggerPresentation.setOptions('boss-animation', presentation_dir="data/presentations/western-cavallotti-riverside")
    level.addSprite(triggerPresentation)

    endPresentation = PresentationTrigger( (15,200), (30,162), (hero,), triggers )
    endPresentation.setOptions('demo-end', presentation_dir="data/presentations/western-cavallotti-riverside")
    level.addSprite(endPresentation)

    level.enableRainEffect()
    level.computeGridMap()
    
    return level