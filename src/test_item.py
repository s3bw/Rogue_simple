import random

from objects import *
import data.materials as mat



# https://gamedev.stackexchange.com/questions/85871/how-should-loot-be-distributed-across-dungeon-levels
# if head & Metal = Helmet
# if head & Wool = Cap
#  Then mention material + item:
#   Gold Helmet/ Steel Helmet
#
# Primary Materials have defence/offense attribute:
# e.g.   50, if gold 50 * 0.2
#            if steel 50 * 0.9
#
# representation based on class
#    --> e.g. tier 1: ^
#    --> e.g. tier 2: n
#    --> e.g. tier 3: M

veg_intensity_dict = {
    'carrot': 0.1,
    'potatoe': 0.5,
    'pumpkin': 0.4
}

veg_wieght_dict = {
    'carrot': 2,
    'potatoe': 3,
    'pumpkin': 4
}

limb_dict = {
    'legs': 15,
    'head': 3
}

limb_priority = {
    'legs': 2,
    'head': 10,
    'chest': 8,
}

representation_dict = {
    'legs': 'h',
    'head': '^'
}

animal_dict = {
    'rabbit': {'size': 2, 'carries': ['veg'], 'strength':0, 'representation': 'r'},    
    'bird': {'size': 1, 'carries': ['pumpkin'], 'strength':0, 'representation': 'm'}
}


def create_tame_animal(x, y, map_area):
    animals = animal_dict.keys()
    animal = random.choice(animals)
    
    hp = animal_dict[animal]['size']*100
    power = animal_dict[animal]['strength']
    representation = animal_dict[animal]['representation']
    
    # Create Item to carry

    animal_object = Creature(hp=hp, power=power, death=creature_death) #, inventory=[carrot])
    final_animal = Object_Place(x, y, map_area, animal, representation, creature=animal_object)
    return final_animal

def create_door(x, y, map_area):
    # Add wood
    materials = mat.Metal_Data['metals'].keys()
    material = random.choice(materials)
    
    name = '{} door'.format(material)
    strength = float(mat.Metal_Data['metals'][material]['strength'])/10.
    weight = mat.Metal_Data['metals'][material]['weight']*10
    
    door_object = Door(lock_strength=strength, lock_durability=weight)
    final_door = Object_Place(x, y, map_area, name, '+', door=door_object)
    return final_door
    
"""
# clothing effect defence, while weapon effects power
def clothing(name, slot, material, tier=1, affect='defense'):
    # Can define by tier. - tier should become rarity
    material_value = material_values[material]
    value = 10*tier*(material_value/2)
    magnitute = limb_priority[slot]
    weight = limb_dict[slot] * material_weights[material]
    representation = representation_dict[slot]
    name = '{} {}'.format(material, name).capitalize()
    
    clothing_item = Item(weight, value)
    clothing_equipment = Equipment(slot, magnitute, affect)
    clothing = Object_Place(None, None, None, name, '^', item=clothing_item, equipment=clothing_equipment)
    return clothing

#  
# def player(attributes for player):
#    return user
#


list_materials = ['wool', 'steel', 'gold']
list_items = [['helmet', 'head'], ['cap', 'head'], ['pants', 'legs']]

index_1 = random.randint(0, len(list_materials) - 1)
index_2 = random.randint(0, len(list_items) - 1)

material = list_materials[index_1]
item_name, slot = list_items[index_2]
tier = float(random.randint(1, 100000)) / 100000
# tier distributions: 1 <= 0.5 <= 0.16 <= 0.041 <= 0.0083 <= 0.0013 <= 0.00019 <= 0.00002     
# print tier
# if tier >= 0.5:
#     print 'Tier 1'
# elif tier >= 0.16:
# if tier 6 add to name 'rare'
tier = random.randint(1, 3)
gen_item = clothing(item_name, slot, material, tier=tier)
print 'Tier: ', tier
print 'Value', 'Weight', 'Name'
print gen_item.item.value, gen_item.item.weight, gen_item.name
print 'Usefulness: ', gen_item.equipment.magnitute
"""