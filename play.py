from src.map import Map
from src.objects import Object_Place, Creature, Item
from src.objects import creature_death
from src.containers import *
from src.item_uses import *
from src.user_functions import *
# from src.message import Message


map = Map(20, 20)
WORLD_CONTAINER.append(map)

#ITEMS
stone_item = Item(weight=10, value=0)
stone = Object_Place(None, None, map, 'Small Stone', 's', item=stone_item)

carrot_item = Item(weight=3, value=5, intensity=0.1, has_use=healing_item)
carrot = Object_Place(None, None, map, 'Carrot', 'v', item=carrot_item)

ring_item = Item(weight=2, value=30)
ring_equip = Equipment('Finger', magnitute=78, affect='power')
ring = Object_Place(None, None, map, 'Ring Of Power', 'o', item=ring_item, equipment=ring_equip)

hat_item = Item(weight=2, value=10)
hat_equip = Equipment('Head', magnitute=20, affect='hp')
hat = Object_Place(5, 3, map, 'Straw Hat', '^', item=hat_item, equipment=hat_equip)

bin = Object_Place(7, 5, map, 'Bin', 'b')


#CREATURES
player = Creature(hp=50, power=5, death=creature_death, inventory=[stone], attire=[ring])
user = Object_Place(5, 5, map, 'Player Character', '@', creature=player)
user_inventory = user.creature.inventory

rabbit_creature = Creature(hp=1000, power=0, death=creature_death, inventory=[stone, carrot, stone])
rabbit = Object_Place(4, 5, map, 'Rabbit', 'r', creature=rabbit_creature)

def build_bar(attribute_name, max, current):
    total_bars = 20
    number_of_bars = int(float(current)/float(max) * total_bars)
    number_pluses = total_bars - number_of_bars
    
    print '{}: '.format(attribute_name), '|'*number_of_bars + '+'*number_pluses

OBJECT_CONTAINER.append(hat)
OBJECT_CONTAINER.append(bin)
OBJECT_CONTAINER.append(rabbit)
OBJECT_CONTAINER.append(user)


def render_map():
    map.refresh_grid()
    for object in OBJECT_CONTAINER:
        if object != user:
            object.draw()    
    
        print (object.x, object.y), object.name, object.representation

    user.draw()
    map.show()

    print [k.name for k in user.creature.attire]    
    print 'Added Power: ', sum(k.equipment.magnitute for k in user.creature.attire if k.equipment.affect == 'hp')
    print [k.name for k in user.creature.inventory]    
    print 'Total value: ', sum(k.item.value for k in user.creature.inventory)
    print 'Total weight: ', sum(k.item.weight for k in user.creature.inventory)
    print 'User HP: {}/{}'.format(str(user.creature.hp), str(user.creature.max_hp))

    
    if rabbit.creature:
        build_bar('rabbit', rabbit.creature.max_hp, rabbit.creature.hp)
    
    print '-'*41

    
game_state = True
while game_state == True:
    render_map()
    
    user_input = raw_input('Where to?')
    if user_input == 'exit':
        break
        
    if user_input == 'equip':
        player_equip_item(user)
        
    if user_input == 'remove':
        player_remove_item(user)
        
    if user_input == 'use':
        player_use_item(user)
        
    if user_input == 'drop':
        player_drop(user)
        
    if user_input == 'pick up':
        player_pick_up(user)
        
    if user_input in MOVES:
        player_move(user, user_input)
        


