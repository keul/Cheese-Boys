# -*- coding: utf-8 -

from cheeseboys.level import GameLevel
from cheeseboys import character
from cheeseboys.level import GameLevel
from cheeseboys.ai.base_brain import BaseStateMachine
from cheeseboys.sprites import CodigoroSign, LevelExit

def load(name, hero):
    level = GameLevel(_(str(name)), (800, 1500))
    level.topleft = (100, 900)
    level.hero = hero

    all = level['all']
    charas = level['charas']
    enemies = level['enemies']
    physical = level['physical']
    exits = level['exits']
    animations = level['animations']
    hero.addToGroups(all, charas, physical)

    enemy1 = character.Character("Max", ("enemy1_sword.png","enemy1.png"), (all,charas,enemies,physical), realSize=(18,25), speed=100., weaponInAndOut=True)
    enemy1.setBrain(BaseStateMachine)
    enemy1.setCombatValues(0, 5)
    enemy2 = character.Character("John", ("enemy1_sword.png","enemy1.png"), (all,charas,enemies,physical), realSize=(18,25), speed=80., weaponInAndOut=True)
    enemy2.setBrain(BaseStateMachine)
    enemy2.setCombatValues(0, 5)
    enemy3 = character.Character("Jack", ("enemy1_sword.png","enemy1.png"), (all,charas,enemies,physical), realSize=(18,25), speed=125., weaponInAndOut=True)
    enemy3.setBrain(BaseStateMachine)
    enemy3.setCombatValues(0, 5)
    enemy4 = character.Character("Roger", ("enemy1_sword.png","enemy1.png"), (all,charas,enemies,physical), realSize=(18,25), speed=160., weaponInAndOut=True)
    enemy4.setBrain(BaseStateMachine)
    enemy4.setCombatValues(0, 5)

    exits1 = LevelExit( (18,208), (36,170), "Western Cavallotti Riverside 1", (1200, 310), (100,290), exits)
    level.addSprite(exits1, (18,208) )

    level.addSprite(hero, (350, 1450))
    level.addSprite(enemy1, (418, 1242))
    level.addSprite(enemy2, (400, 300))
    level.addSprite(enemy3, (320, 210))
    level.addSprite(enemy4, (250, 520))

    level.addPhysicalBackground( (118,1338), (235, 1130) )
    level.addPhysicalBackground( (642,1338), (310, 1130) )
    
    level.addAnimations(((110,980),(623, 1284),(704, 1149),(30, 1299),(610, 869),(157, 527),(642, 357),(5, 363)), 'water-wave')
    
    # BBB: this isn't an animation... why don't use normal sprite handling like characters?
    level.addAnimation( (535,1475), CodigoroSign((535,1475), (80,53), animations, physical) )

    level.enableRainEffect()
    
    return level