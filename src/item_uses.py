# from objects import *

Tense_Dict = { 
    'eat' :{
        'present': 'eat',
        'past': 'ate'
    },
    'drink':{
        'present': 'drink',
        'past': 'quaffed'
    }
}

def healing_item(item_used, used_on_creature, verb):
    heal = int(used_on_creature.max_hp * item_used.intensity)
    if used_on_creature.hp == used_on_creature.max_hp:
        print 'Already at full health'
        used_on_creature.inventory.append(item_used.owner)
    else:
        print '{} {} the {}!'.format(used_on_creature.owner.name, Tense_Dict[verb]['past'], item_used.owner.name)
        used_on_creature.hp += heal
    