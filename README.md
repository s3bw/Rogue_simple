# Rogue_simple
A classic Roguelike

## TODO:[Complexity out of 10, Time out of 10]
- Stairs [2,2]
- Creature-limbs [4,6]
- Attack-Targeting [6,5]
- Map-gen round 2 [8,10]
- ai [6,4]
- Distance to calculation [3,3]
    --> Use to build bars of objects nearby. [2,1]

## To Fix/Do:

 - Doors appearing adjacent to walls. (Can't enter this room, especially if there is one door).
 - Doors still depreciate after their lock has given-way, we can have the door become a smashed object, if it reaches `-20` for eg.
 - Need to Drop items from attire, not just inventory.
 - hp increasing items need to do % based increases - this is to aid Creatures with less than max Health.
 - Usable items need methods of use (eat, drink, throw)
 
## The Vegitable Idea: 

```
from objects import *

material_dict = {
    'wool': 2,
    'steel': 10
}

limb_dict = {
    'legs': 15,
    'head': 3
}

representation_dict = {
    'legs': 'h',
    'head': '^'
}

def clothing(name, slot, material, tier=1):
    # Can define by tier.
    material_value = material_dict[material]
    value = 10*tier*(material_value/2)
    magnitute = 20*tier
    weight = limb_dict[slot] * material_value
    representation = representation_dict[slot]
    
    clothing_item = Item(weight=2, value)
    clothing_equipment = Equipment(slot, magnitute, affect='hp')
    clothing = Object_Place(None, None, None, name, '^', item=clothing_item, equipment=clothing_equipment)
    return clothing

import wearables

helmet = wearables.clothing('Helmet', 'head', 'steel', tier=3)
hat = wearables.clothing('Cap', 'head', 'wool', tier=1)
trousers = wearables.clothing('Wool Pants', 'legs', 'wool', tier=2)



```
