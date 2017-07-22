from src.map import Map
from src.objects import Object_Place, Creature, Item
from src.objects import creature_death
from src.containers import *
# from src.message import Message


moves = {
    'up': [-1,0],
    'down': [1,0],
    'left': [0,-1],
    'right': [0,1]
}

map = Map(10, 10)
WORLD_CONTAINER.append(map)

player = Creature(hp=50, power=5, death=creature_death, inventory=[])
user = Object_Place(5, 5, map, 'Player Character', '@', creature=player)
user_inventory = user.creature.inventory
OBJECT_CONTAINER.append(user)

stone_item = Item(weight=10, value=0)
stone = Object_Place(None, None, map, 'Small Stone', 'o', item=stone_item)

carrot_item = Item(weight=3, value=5)
carrot = Object_Place(None, None, map, 'Carrot', 'v', item=carrot_item)

rabbit_creature = Creature(hp=10, power=0, death=creature_death, inventory=[stone, carrot, stone])
rabbit = Object_Place(3, 5, map, 'Rabbit', 'r', creature=rabbit_creature)
OBJECT_CONTAINER.append(rabbit)

user_inventory.append(stone)

hat_item = Item(weight=2, value=10)
hat = Object_Place(5, 3, map, 'Straw Hat', '^', item=hat_item)
OBJECT_CONTAINER.append(hat)

bin = Object_Place(7, 5, map, 'Bin', 'b')
OBJECT_CONTAINER.append(bin)



def render_map():
    map.refresh_grid()
    for object in OBJECT_CONTAINER:
        if object != user:
            object.draw()    
    
        print (object.x, object.y), object.name, object.representation
        
    user.draw()
    map.show()
    print '-'*41

    
def player_move(user_input):
    dx, dy = moves[user_input]
    x = user.x + dx
    y = user.y + dy
    
    target = None
    for object in OBJECT_CONTAINER:
        if object.creature is not None and object.x == x and object.y ==y:
            target = object
            break
        
    if target is not None:
        user.creature.attack(target)
        
    else:
        user.move(dx, dy)
        
def player_drop():
    if len(user_inventory) > 1:
        print 'What item do you want to drop?'
        for index, user_item in enumerate(user_inventory):
            print '{}. {}'.format(index, user_item.name)
        item_to_drop = raw_input('Item: ')
        
        for user_item in user_inventory:
            if item_to_drop == user_item.name:
                user_inventory.remove(user_item)
                user_item.item.drop(user.x, user.y)
                
    elif user_inventory:
        only_item = user_inventory[0]
        user_inventory.remove(only_item)
        only_item.item.drop(user.x, user.y)
        
def player_pick_up():
    for object in OBJECT_CONTAINER:
        if object != user and object.x == user.x and object.y == user.y and object.item:
            user_inventory.append(object)
            object.item.pick_up()
            print 'Picked up {}.'.format(object.name)


game_state = True
while game_state == True:
    render_map()
    
    user_input = raw_input('Where to?')
    if user_input == 'exit':
        break
        
    if user_input == 'drop':
        player_drop()
        
    if user_input == 'pick up':
        player_pick_up()
        
    if user_input in moves:
        player_move(user_input)
        



# print map.grid[5][5].blocked