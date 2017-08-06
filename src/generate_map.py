from containers import *
from map_class import Grid
from object_creator import Create

# needed to object test
from objects import *

from item_uses import *

def spawn_player(x, y, z):
    # Starting item should depend on class
    long_sword_item = Item(weight=400, value=60)
    sword_equip = Equipment(['Main-Hand','Off-Hand'], magnitute=1250, optional_slot=True, equipped_slot='Main-Hand', affect_attribute='power')
    sword = Object_Place(None, None, None, 'The Dragonslayer', '/', item=long_sword_item, equipment=sword_equip)
    
    crit_glyph_item = Item(weight=2, value=30, intensity=0.5, has_use=inscribe_glyph, use_verb='inscribe', inscribe_affect='crit')
    crit_glyph = Object_Place(None, None, None, 'Crit Glyph', '*', item=crit_glyph_item)
    
    power_glyph_item = Item(weight=2, value=30, intensity=0.5, has_use=inscribe_glyph, use_verb='inscribe', inscribe_affect='magnitute')
    power_glyph = Object_Place(None, None, None, 'Power Glyph', '*', item=power_glyph_item)
    
    ring_item = Item(weight=2, value=30)
    ring_equip = Equipment(['Finger'], magnitute=50, equipped_slot='Finger', affect_attribute='hp')
    ring = Object_Place(None, None, None, 'Ring Of Health', 'o', item=ring_item, equipment=ring_equip)
    
    food = Create(z).food()
    player = Creature(hp=50, power=5, death=creature_death, inventory=[food, crit_glyph, power_glyph], attire=[sword, ring])
    user = Object_Place(x, y, z, 'Player Character', '@', creature=player)
    user.creature.hp -= 20
    return user 
    


def generate(grid_z, lower=True, start_game=False):
    # GRID defines the grid size, generate with define the biome, 
    # Thus: this is where we change the grid size and we wont pass it into generate.
    restricted_places = None
    if not start_game:
        restricted_places = [(object.x, object.y) for object in OBJECT_CONTAINER]
        [(entrance_x, entrance_y)] = restricted_places
        
    map_area = Grid(grid_biome='village', first_grid=start_game, building_restriction=restricted_places)
    WORLD_CONTAINER.append(map_area)
    
    
    # Stairs
    if grid_z > 0:
        stair_object = Stairs(not lower)
        entrance = Object_Place(entrance_x, entrance_y, grid_z, 'Up Stair', '<', stairs=stair_object)
        if not lower:
            stair_object = Stairs(not lower)
            entrance = Object_Place(entrance_x, entrance_y, grid_z, 'Down Stair', '>', stairs=stair_object)            
        OBJECT_CONTAINER.append(entrance)

    exit_x, exit_y = map_area.exit_point
    stair_object = Stairs(lower)
    exit = Object_Place(exit_x, exit_y, grid_z, 'Down Stair', '>', stairs=stair_object)
    if not lower and grid_z > 0:
        stair_object = Stairs(lower)
        exit = Object_Place(exit_x, exit_y, grid_z, 'Up Stair', '<', stairs=stair_object)
    OBJECT_CONTAINER.append(exit)
        
    

    
    make_weapon = Create(7, 5, grid_z).weapon()
    OBJECT_CONTAINER.append(make_weapon)
    
    ring_item = Item(weight=2, value=30)
    ring_equip = Equipment(['Finger'], magnitute=78, affect_attribute='power')
    ring = Object_Place(None, None, grid_z, 'Ring Of Power', 'o', item=ring_item, equipment=ring_equip)
    
    animal_object = Creature(hp=12, power=5, death=creature_death, inventory=[], attire=[ring])
    final_animal = Object_Place(5, 7, grid_z, 'pig', 'p', creature=animal_object)
    OBJECT_CONTAINER.append(final_animal)

  #  if start_game == True:
        #Place the player in the user_space
        
    # Place Objects in spaces
    for building in map_area.rooms:
        if hasattr(building.room, 'user_space'):
            print 'user spawned'
            x, y = building.room.user_space
            user = spawn_player(x, y, grid_z)
            OBJECT_CONTAINER.insert(0, user)
            
            x, y = building.room.bin_space
            food = Create(grid_z).food()
            bucket_storage = Storage(capacity=6, contains=[food], infinity_id='user_house', is_infinity=True)
            bucket = Object_Place(x, y, grid_z, 'bucket', 'u', storage=bucket_storage)
            OBJECT_CONTAINER.append(bucket)
            
        # should pass 'structure_value' into the creation property distribution
        structure_value = building.room.value
        for (x, y) in building.room.door_space:
            # need unlocked doors on shop and low value houses
            place = Create(x, y, grid_z, structure_value)
            door = place.door()
            OBJECT_CONTAINER.append(door)
            
        for (x, y) in building.room.object_space:
            place = Create(x, y, grid_z, structure_value)
            animal = place.tame_animal()
            # if structure_value > 80:
                # animal = obj.create_tame_animal(x, y, map_area)
            # elif structure_value < 10:
                # animal = obj.create_tame_animal(x, y, map_area)
            # else:
                # animal = obj.create_tame_animal(x, y, map_area)
            OBJECT_CONTAINER.append(animal)

 
