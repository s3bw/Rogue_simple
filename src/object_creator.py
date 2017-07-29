import random
from objects import *
from item_uses import *
import data.materials as mat
import data.animals as ani





# Make these functions before making data.
def create_food(x, y, map_area):
    food_item = Item(weight=3, value=5, intensity=0.1, has_use=healing_item)
    food = Object_Place(x, y, map_area, 'Carrot', 'v', item=food_item)
    return food

    
def create_tame_animal(x, y, map_area):
    animal_keys = ani.Animal_Data.keys()
    animal = random.choice(animal_keys)
    
    hp = ani.Animal_Data[animal]['size']*100
    power = ani.Animal_Data[animal]['strength']
    representation = ani.Animal_Data[animal]['representation']
    
    # Create Item to carry

    animal_object = Creature(hp=hp, power=power, death=creature_death) #, inventory=[carrot])
    final_animal = Object_Place(x, y, map_area, animal, representation, creature=animal_object)
    return final_animal

    
def create_door(x, y, map_area):
    # Add wood
    material_keys = mat.Metal_Data['metals'].keys()
    material = random.choice(material_keys)
    
    name = '{} door'.format(material)
    strength = float(mat.Metal_Data['metals'][material]['strength'])/10.
    weight = mat.Metal_Data['metals'][material]['weight']*1
    
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

# hat_item = Item(weight=2, value=10)
# hat_equip = Equipment('Head', magnitute=20, affect='hp')
# hat = Object_Place(None, None, map_area, 'Straw Hat', '^', item=hat_item, equipment=hat_equip)

stone_item = Item(weight=10, value=0)
stone = Object_Place(None, None, map_area, 'Small Stone', 's', item=stone_item)

ring_item = Item(weight=2, value=30)
ring_equip = Equipment('Finger', magnitute=78, affect='power')
ring = Object_Place(None, None, map_area, 'Ring Of Power', 'o', item=ring_item, equipment=ring_equip)


"""