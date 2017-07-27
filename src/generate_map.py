from map_class import Grid
from containers import *
from objects import *
from item_uses import *

from test_item import create_door, create_tame_animal


def generate(horrizontal, vertical, biome):
    map_area = Grid(horrizontal, vertical, biome)

    # Equiped or in inventory.

    # hat_item = Item(weight=2, value=10)
    # hat_equip = Equipment('Head', magnitute=20, affect='hp')
    # hat = Object_Place(None, None, map_area, 'Straw Hat', '^', item=hat_item, equipment=hat_equip)

    for building in map_area.rooms:
        # should pass in this structure value into the creation distribution
        structure_value = building.room.value
        
        for (x, y) in building.room.door_space:
            if structure_value > 80:
                door = create_door(x, y, map_area)
            elif structure_value < 10:
                door = create_door(x, y, map_area)
            else:
                door = create_door(x, y, map_area)
            OBJECT_CONTAINER.append(door)
            
        for (x, y) in building.room.object_space:
            if structure_value > 80:
                animal = create_tame_animal(x, y, map_area)
            elif structure_value < 10:
                animal = create_tame_animal(x, y, map_area)
            else:
                animal = create_tame_animal(x, y, map_area)
            OBJECT_CONTAINER.append(animal)
                
    WORLD_CONTAINER.append(map_area)


#ITEMS
"""
stone_item = Item(weight=10, value=0)
stone = Object_Place(None, None, map_area, 'Small Stone', 's', item=stone_item)

carrot_item = Item(weight=3, value=5, intensity=0.1, has_use=healing_item)
carrot = Object_Place(None, None, map_area, 'Carrot', 'v', item=carrot_item)

ring_item = Item(weight=2, value=30)
ring_equip = Equipment('Finger', magnitute=78, affect='power')
ring = Object_Place(None, None, map_area, 'Ring Of Power', 'o', item=ring_item, equipment=ring_equip)

hat_item = Item(weight=2, value=10)
hat_equip = Equipment('Head', magnitute=20, affect='hp')
hat = Object_Place(None, None, map_area, 'Straw Hat', '^', item=hat_item, equipment=hat_equip)

bin = Object_Place(7, 5, map_area, 'Bin', 'b')

#DOOR
irondoor_door = Door()
irondoor = Object_Place(5, 6, map_area, 'Iron Door', '+', door=irondoor_door)


#CREATURES
rabbit_creature = Creature(hp=1000, power=0, death=creature_death, inventory=[carrot])
rabbit = Object_Place(4, 5, map_area, 'Rabbit', 'r', creature=rabbit_creature)
OBJECT_CONTAINER.append(rabbit)

rabbit_creature = Creature(hp=250, power=0, death=creature_death, inventory=[stone, carrot, stone])
rabbit = Object_Place(3, 4, map_area, 'Rabbit', 'r', creature=rabbit_creature)

# OBJECT_CONTAINER.append(hat)
OBJECT_CONTAINER.append(bin)
OBJECT_CONTAINER.append(irondoor)
OBJECT_CONTAINER.append(rabbit)
"""
