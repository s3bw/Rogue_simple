import src.generate_map as map_gen

from src.containers import OBJECT_CONTAINER
from src.containers import WORLD_CONTAINER

from src.objects import *
from src.user_functions import *
# from src.message import Message

map_gen.generate(20, 20, 'village')

depth_index = 0
current_area = WORLD_CONTAINER[depth_index]

#PLAYER and PLAYER ITEMS
long_sword_item = Item(weight=5, value=60)
sword_equip = Equipment('Hand', magnitute=125, affect='power')
sword = Object_Place(None, None, current_area, 'Long Sword', '/', item=long_sword_item, equipment=sword_equip)

player = Creature(hp=50, power=5, death=creature_death, inventory=[], attire=[sword])
user = Object_Place(5, 5, current_area, 'Player Character', '@', creature=player)
OBJECT_CONTAINER.append(user)

print [n.name for n in OBJECT_CONTAINER]
print sword.equipment.is_equipped


def build_bar(attribute_name, max, current):
    total_bars = 20
    number_of_bars = int(float(current)/float(max) * total_bars)
    number_pluses = total_bars - number_of_bars
    
    print '{}: '.format(attribute_name), '|'*number_of_bars + '+'*number_pluses


def render_map():
    
    current_area.refresh_grid()
    for object in OBJECT_CONTAINER:
        if object != user:
            object.draw()
    
        print (object.x, object.y), object.name, object.representation

    user.draw()
    current_area.show()

    print 'Attire: ', [k.name for k in user.creature.attire]    
    print 'Added Power: ', sum(k.equipment.magnitute for k in user.creature.attire if k.equipment.affect == 'power')
    print 'Inventory: ', [k.name for k in user.creature.inventory]    
    print 'Net Worth: ', sum(k.item.value for k in user.creature.inventory + user.creature.attire)
    print 'Net Weight: ', sum(k.item.weight for k in user.creature.inventory + user.creature.attire)
    print 'User HP: {}/{}'.format(str(user.creature.hp), str(user.creature.max_hp))
    
    for object in OBJECT_CONTAINER:
        if object.creature:
            build_bar(object.name, object.creature.max_hp, object.creature.hp)

    print '-'*41

    
# key presses 
game_state = True
while game_state == True:
    render_map()
    
    user_input = raw_input('Where to?')
    if user_input == 'exit':
        break
        
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
        


