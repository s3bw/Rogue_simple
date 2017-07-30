from containers import *
from map_class import Grid
from object_creator import Create

# needed to object test
from objects import *

def generate(horrizontal, vertical, biome):
    map_area = Grid(horrizontal, vertical, biome)
    place = Create(map_area)

    food = place.food()

    bucket_storage = Storage(capacity=25, contains=[food])
    bucket = Object_Place(5, 3, map_area, 'bucket', 'u', storage=bucket_storage)
    OBJECT_CONTAINER.append(bucket)
    
    make_weapon = Create(7, 5, map_area).weapon()
    OBJECT_CONTAINER.append(make_weapon)
    
    ring_item = Item(weight=2, value=30)
    ring_equip = Equipment(['Finger'], magnitute=78, affect='power')
    ring = Object_Place(None, None, map_area, 'Ring Of Power', 'o', item=ring_item, equipment=ring_equip)
    
    animal_object = Creature(hp=12, power=5, death=creature_death, inventory=[], attire=[ring])
    final_animal = Object_Place(5, 7, map_area, 'pig', 'p', creature=animal_object)
    OBJECT_CONTAINER.append(final_animal)

    for building in map_area.rooms:
        # should pass 'structure_value' into the creation property distribution
        structure_value = building.room.value
        
        for (x, y) in building.room.door_space:
            place = Create(x, y, map_area, structure_value)
            door = place.door()
            OBJECT_CONTAINER.append(door)
            
        for (x, y) in building.room.object_space:
            place = Create(x, y, map_area, structure_value)
            animal = place.tame_animal()
            # if structure_value > 80:
                # animal = obj.create_tame_animal(x, y, map_area)
            # elif structure_value < 10:
                # animal = obj.create_tame_animal(x, y, map_area)
            # else:
                # animal = obj.create_tame_animal(x, y, map_area)
            OBJECT_CONTAINER.append(animal)
                
    WORLD_CONTAINER.append(map_area)
