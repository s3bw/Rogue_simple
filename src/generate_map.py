from map_class import Grid
from containers import *
import object_creator as obj

# needed to object test
from objects import *

def generate(horrizontal, vertical, biome):
    map_area = Grid(horrizontal, vertical, biome)

    food = obj.create_food(None, None, map_area)
    
    bucket_storage = Storage(capacity=25, contains=[food])
    bucket = Object_Place(5, 3, map_area, 'bucket', 'u', storage=bucket_storage)
    OBJECT_CONTAINER.append(bucket)
    
    food_1 = obj.create_food(None, None, map_area)
    
    ring_item = Item(weight=2, value=30)
    ring_equip = Equipment('Finger', magnitute=78, affect='power')
    ring = Object_Place(None, None, map_area, 'Ring Of Power', 'o', item=ring_item, equipment=ring_equip)
    
    animal_object = Creature(hp=12, power=5, death=creature_death, inventory=[food_1], attire=[ring])
    final_animal = Object_Place(5, 7, map_area, 'pig', 'p', creature=animal_object)
    OBJECT_CONTAINER.append(final_animal)
    
    # Make items Equiped or in inventory.
    obj.create_food(5, 6, map_area)

    for building in map_area.rooms:
        # should pass 'structure_value' into the creation property distribution
        structure_value = building.room.value
        
        for (x, y) in building.room.door_space:
            if structure_value > 80:
                door = obj.create_door(x, y, map_area)
            elif structure_value < 10:
                door = obj.create_door(x, y, map_area)
            else:
                door = obj.create_door(x, y, map_area)
            OBJECT_CONTAINER.append(door)
            
        for (x, y) in building.room.object_space:
            if structure_value > 80:
                animal = obj.create_tame_animal(x, y, map_area)
            elif structure_value < 10:
                animal = obj.create_tame_animal(x, y, map_area)
            else:
                animal = obj.create_tame_animal(x, y, map_area)
            OBJECT_CONTAINER.append(animal)
                
    WORLD_CONTAINER.append(map_area)
