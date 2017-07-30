import random
from objects import *
from item_uses import *
import data.materials as mat
import data.animals as ani
import data.weapons as weap


class Select_Material:
    def __init__(self, threshold_value=0, threshold_field='strength', material_list=None, filter_type='less_than'):
        self.threshold_value = threshold_value
        self.threshold_field = threshold_field
        self.filter_type = filter_type
        
        self.material_list = material_list        
        self.material = self.get_materials()

    def choose_material(self, materials_dict):
        materials_dict = self.filter_less_than(materials_dict)
        material_keys = materials_dict.keys()
        chosen_material = random.choice(material_keys)        
        return chosen_material, materials_dict[chosen_material]        
        
    def get_materials(self):
        materials = {}        
        if 'metal' in self.material_list:
            materials.update(mat.Metal_Data)
        if 'wood' in self.material_list:
            materials.update(mat.Wood_Data)
        if 'textile' in self.material_list:
            materials.update(mat.Textile_Data)            
        return self.choose_material(materials)        
        
    def filter_less_than(self, materials_dict):
        """
        Finds the max value in the field to filter by and multiplies the max by the 'threshold_value'.
        
        :param materials_dict: (dict) of materials to select from. (e.g. {'iron' : { 'value': 6, 'weight': 28})
        :return: the materials_dict after filtering the lower values.
        """
        max_in_field = max({
            materials_dict[key][self.threshold_field] 
            for (key, val) in materials_dict.iteritems()
        })

        materials_dict = {
            material: value 
            for material, value in materials_dict.iteritems() 
            if value[self.threshold_field] >= (max_in_field * self.threshold_value)
        }
        return materials_dict
        
    def get(self):
        return self.material


class Create:
    def __init__(self, x=None, y=None, area=None, rarity_value=0):
        self.x = x
        self.y = y 
        self.area = area
        
        self.rarity_value = rarity_value/100.
    
    # Make these functions before making data.
    def food(self):
        food_item = Item(weight=3, value=5, intensity=0.1, has_use=healing_item)
        food = Object_Place(self.x, self.y, self.area, 'Carrot', 'v', item=food_item)
        return food
        
    def tame_animal(self):
        animal_keys = ani.Animal_Data.keys()
        animal = random.choice(animal_keys)
        
        hp = ani.Animal_Data[animal]['size']*100
        power = ani.Animal_Data[animal]['strength']
        representation = ani.Animal_Data[animal]['representation']
        
        # Create Item to carry

        animal_object = Creature(hp=hp, power=power, death=creature_death) #, inventory=[carrot])
        final_animal = Object_Place(self.x, self.y, self.area, animal, representation, creature=animal_object)
        return final_animal
        
    def door(self):
        material, attributes = Select_Material(self.rarity_value, material_list=['metal', 'wood']).get()
        strength = attributes['strength']/40.
        weight = attributes['weight']
        
        name = '{} door'.format(material)       
        door_object = Door(lock_strength=strength, lock_durability=weight)
        final_door = Object_Place(self.x, self.y, self.area, name, '+', door=door_object)
        return final_door
        
    def weapon(self):
        weapon_keys = weap.Melee_Weapon_Data.keys()
        weapon_name = random.choice(weapon_keys)
        weapon = weap.Melee_Weapon_Data[weapon_name]
        
        material_list = weapon['mat_types']
        material, attributes = Select_Material(self.rarity_value, material_list=material_list).get()
        
        # Attribute Calculations
        weight = (attributes['weight'] * weapon['size']) / 15
        value = (attributes['value'] * weapon['size']) / 2.5
        magnitute = attributes['strength'] * 3
        weapon_name = '{} {}'.format(material,weapon_name).capitalize()
        
        slots = ['Main-Hand', 'Off-Hand']
        optional_slot = True
        if weapon['size_string'] and weapon['size_string'] == 'long':
            optional_slot = False
        
        weapon_item = Item(weight=weight, value=value)
        weapon_equip = Equipment(slots, magnitute=magnitute, optional_slot=optional_slot, affect='power')
        weapon = Object_Place(self.x, self.y, self.area, weapon_name, '/', item=weapon_item, equipment=weapon_equip)
        return weapon

    
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