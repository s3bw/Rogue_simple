# from objects import *
from user_functions import check_inventory

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

def inscribe_glyph(inscription, used_on_creature, verb):
    creatures_items = used_on_creature.inventory + used_on_creature.attire
    inscribing = check_inventory(creatures_items)
    if inscribing.equipment and inscribing.equipment.can_inscribe:
        print 'The chosen item is:', inscribing.name
        inscribing.equipment.inscriptions.append(inscription)
        print inscribing.equipment.inscriptions
    # Saves item if used incorrectly
    else:
        print "Can't Inscribe That Item!"
        used_on_creature.inventory.append(inscription.owner)

def healing_item(item_used, used_on_creature, verb):
    heal = int(used_on_creature.max_hp * item_used.intensity)
    if used_on_creature.hp == used_on_creature.max_hp:
        print 'Already at full health'
        used_on_creature.inventory.append(item_used.owner)
    else:
        print '{} {} the {}!'.format(used_on_creature.owner.name, Tense_Dict[verb]['past'], item_used.owner.name)
        used_on_creature.hp += heal
    