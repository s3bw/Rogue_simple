from map_class import Grid
from containers import *
import object_creator as obj


def generate(horrizontal, vertical, biome):
    map_area = Grid(horrizontal, vertical, biome)

    # Make items Equiped or in inventory.
    obj.create_food(5, 6, map_area)

    for building in map_area.rooms:
        # should pass in this structure value into the creation distribution
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
