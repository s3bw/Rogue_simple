# from objects import *

def healing_item(item_used, creature_using_item):
    heal = int(creature_using_item.max_hp * item_used.intensity)
    if creature_using_item.hp == creature_using_item.max_hp:
        print 'Already at full health'
        creature_using_item.inventory.append(item_used.owner)
    else:
        print 'That {} was delicious!'.format(item_used.owner.name)
        creature_using_item.hp += heal
    