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
stone = Object_Place(None, None, map, 'Small Stone', 'o', item=stone_item)

carrot_item = Item(weight=3, value=5, intensity=0.1, has_use=healing_item)
carrot = Object_Place(None, None, map, 'Carrot', 'v', item=carrot_item)

hat_item = Item(weight=2, value=10)
hat = Object_Place(5, 3, map, 'Straw Hat', '^', item=hat_item)

bin = Object_Place(7, 5, map, 'Bin', 'b')


#CREATURES
player = Creature(hp=50, power=5, death=creature_death, inventory=[stone])
user = Object_Place(5, 5, map, 'Player Character', '@', creature=player)
user_inventory = user.creature.inventory

rabbit_creature = Creature(hp=10, power=0, death=creature_death, inventory=[stone, carrot, stone])
rabbit = Object_Place(3, 5, map, 'Rabbit', 'r', creature=rabbit_creature)


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
    print '-'*41

    
game_state = True
while game_state == True:
    render_map()
    
    user_input = raw_input('Where to?')
    if user_input == 'exit':
        break
        
    if user_input == 'use':
        player_use_item(user)
        
    if user_input == 'drop':
        player_drop(user)
        
    if user_input == 'pick up':
        player_pick_up(user)
        
    if user_input in MOVES:
        player_move(user, user_input)
        


