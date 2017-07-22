from src.containers import *
from src.objects import *

MOVES = {
    'up': [-1,0],
    'down': [1,0],
    'left': [0,-1],
    'right': [0,1]
}

def check_inventory(user_inventory):
    if len(user_inventory) > 1:
        print 'Select an item.'
        for index, item_in_bag in enumerate(user_inventory):
            print '{}. {}'.format(index, item_in_bag.name)
        selected_item = raw_input('Item: ')
        
        for item_in_bag in user_inventory:
            if selected_item == item_in_bag.name:
                return item_in_bag
                
    elif user_inventory:
        last_item = user_inventory[0]
        return last_item

def player_move(user, user_input):
    dx, dy = MOVES[user_input]
    x = user.x + dx
    y = user.y + dy
    
    target = None
    for object in OBJECT_CONTAINER:
        if object.creature is not None and object.x == x and object.y == y:
            target = object
            break
        
    if target is not None:
        user.creature.attack(target)
        
    else:
        user.move(dx, dy)
        
        
def player_drop(user):
    user_inventory = user.creature.inventory
    selected = check_inventory(user_inventory)
    
    user_inventory.remove(selected)
    selected.item.drop(user.x, user.y)


def player_use_item(user):
    user_inventory = user.creature.inventory
    selected = check_inventory(user_inventory)
    
    if selected.item.has_use:
        user_inventory.remove(selected)
        selected.item.use(user)
        
def player_pick_up(user):
    user_inventory = user.creature.inventory

    for object in OBJECT_CONTAINER:
        if object != user and object.x == user.x and object.y == user.y and object.item:
            user_inventory.append(object)
            object.item.pick_up()
            print 'Picked up {}.'.format(object.name)
            