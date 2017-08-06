import src.generate_map as map_gen

from src.containers import OBJECT_CONTAINER
from src.containers import WORLD_CONTAINER

from src.objects import *
from src.user_functions import *
# from src.message import Message

def build_bar(attribute_name, max, current):
    total_bars = 20
    number_of_bars = int(float(current)/float(max) * total_bars)
    number_pluses = total_bars - number_of_bars
    
    print '{}: '.format(attribute_name), '|'*number_of_bars + '+'*number_pluses


def render_map():
    current_area = WORLD_CONTAINER[0]
    
    current_area.refresh_grid()
    for object in OBJECT_CONTAINER:
        if object != user:
            object.draw()
        
        if not object.storage:
            print (object.x, object.y), object.name, object.representation
        else:
            print (object.x, object.y), object.name, object.representation, object.storage.remaining_capacity, object.storage.max_capacity

    user.draw()
    current_area.show()

    for x in user.creature.attire:
        print x.equipment.equipped_slot
    
    print 'Depth:', user.active_z, len(WORLD_CONTAINER)
    print 'Attire: ', [k.name for k in user.creature.attire]    
    print 'Added Power: ', sum(k.equipment.magnitute for k in user.creature.attire if k.equipment.affect_attribute == 'power')
    print 'Inventory: ', [k.name for k in user.creature.inventory]    
    print 'Net Worth: ', sum(k.item.value for k in user.creature.inventory + user.creature.attire)
    print 'Net Weight: ', sum(k.item.weight for k in user.creature.inventory + user.creature.attire)
    print 'User HP: {}/{}'.format(str(user.creature.hp), str(user.creature.max_hp))
    
    
    for object in OBJECT_CONTAINER:
        if object.creature:
            build_bar(object.name, object.creature.max_hp, object.creature.hp)

    print '-'*41


    
depth = 0
map_gen.generate(grid_z=depth, start_game=True)
user = OBJECT_CONTAINER[0]

# key presses
game_state = True
while game_state == True:
    render_map()
    
    user_input = raw_input('Where to?')
    if user_input == 'exit':
        save_infinity_chests()
        break
        
    if user_input == '>' or user_input == '<':
        player_travel_z(user, user.active_z)
        
    if user_input == 'open' or user_input == 'o':
        player_query_storage(user)
        
    if user_input == 'close' or user_input == 'c':
        player_toggle_door(user)
        
    if user_input == 'equip' or user_input == 'e':
        player_equip_item(user)
        
    if user_input == 'remove':
        player_remove_item(user)
        
    if user_input == 'use' or user_input == 'u':
        player_use_item(user)
        
    if user_input == 'drop' or user_input == 'd':
        player_drop(user)
        
    if user_input == 'get' or user_input == 'g':
        player_pick_up(user)
        
    if user_input in MOVES:
        player_move(user, user_input)
        