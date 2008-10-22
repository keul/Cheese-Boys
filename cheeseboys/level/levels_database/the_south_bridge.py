# -*- coding: utf-8 -

from cheeseboys.level import GameLevel
from cheeseboys.pygame_extensions import GameGroup
from cheeseboys import character
from cheeseboys.level import GameLevel
from cheeseboys.ai.base_brain import BaseStateMachine
from cheeseboys.sprites import CodigoroSign

def load(name, hero):
    level = GameLevel(_(str(name)), (800, 1500))
    level.topleft = (100, 900)
    
    all = GameGroup("all")
    dead = GameGroup("dead", drawable=True, updatable=True)
    physical = GameGroup("physical", drawable=True, updatable=True)
    charas = GameGroup("charas")
    enemies = GameGroup("enemies")
    animations = GameGroup("animations", drawable=True, updatable=True)
    top_animations = GameGroup("top_animations", drawable=True, updatable=True)
    speech = GameGroup("speech", drawable=True, updatable=True)
    level_text = GameGroup("level_text")

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

    level.addSprite(hero, (350, 1450))
    level.addSprite(enemy1, (418, 1242))
    level.addSprite(enemy2, (400, 300))
    level.addSprite(enemy3, (320, 210))
    level.addSprite(enemy4, (250, 520))

    level.addGroup(dead, zindex=5)
    level.addGroup(physical, zindex=10)
    level.addGroup(charas, zindex=10)
    level.addGroup(enemies)
    level.addGroup(animations, zindex=3)
    level.addGroup(top_animations, zindex=20)
    level.addGroup(speech, zindex=15)
    level.addGroup(level_text, zindex=30)

    level.addPhysicalBackground( (118,1338), (235, 1130) )
    level.addPhysicalBackground( (642,1338), (310, 1130) )
    
    level.addAnimations(((110,980),(623, 1284),(704, 1149),(30, 1299),(610, 869),(157, 527),(642, 357),(5, 363)), 'water-wave')
    level.addAnimation( (535,1475), CodigoroSign((535,1475), (80,53), animations, physical) )

    level.enableRainEffect()
    
    return level