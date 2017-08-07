from containers import *
from objects import *

INFINITY_DATA = '.\\src\\infinity_data\\'

MOVES = {
    'up': [-1,0],
    'down': [1,0],
    'left': [0,-1],
    'right': [0,1]
}

def check_inventory(inventory_list):
    if len(inventory_list) > 1:
        print 'Select an item.'
        for index, item_in_bag in enumerate(inventory_list):
            print '{}. {}'.format(index, item_in_bag.name)
        selected_item = raw_input('Item: ')
        
        for item_in_bag in inventory_list:
            if selected_item == item_in_bag.name:
                return item_in_bag
                
    elif inventory_list:
        last_item = inventory_list[0]
        return last_item

def player_move(user, user_input):
    dx, dy = MOVES[user_input]
    x = user.x + dx
    y = user.y + dy
    
    target = None
    for object in OBJECT_CONTAINER:
        valid_target = ((object.door is not None or object.creature is not None) and object.x == x and object.y == y)
        if valid_target:
            target = object
            break
        
    if target is not None:
        if target.creature:
            user.creature.attack(target)
            
        elif not target.door.open:
            target.door.reduce_durability(user.creature.base_power)
        
        # Door is open
        else:
            user.move(dx, dy)        
    else:
        user.move(dx, dy)


def user_stats():
    user = OBJECT_CONTAINER[0]
    print 'Attire: ', [k.name for k in user.creature.attire]
    print 'Inventory: ', [k.name for k in user.creature.inventory]
    print 'Added Power: ', sum(k.equipment.magnitute for k in user.creature.attire if k.equipment.affect_attribute == 'power')
    print 'Net Worth: ', sum(k.item.value for k in user.creature.inventory + user.creature.attire)
    print 'Net Weight: ', sum(k.item.weight for k in user.creature.inventory + user.creature.attire)
    print 'User Defence: {}'.format(str(user.creature.defence))
        
def save_infinity_chests():
    for object in OBJECT_CONTAINER:
        if object.storage and object.storage.is_infinity:
            infinity_data = shelve.open('{}game_save.txt'.format(INFINITY_DATA))
            infinity_data[object.storage.infinity_id] = object.storage.contains
            infinity_data.close()

def player_query_storage(user):
    area_around_user = [(dx + user.x, dy + user.y) for (dx, dy) in OFF_SETS]
    user_input = raw_input('Would you like to storage or take? (S/T)')
    
    if user_input == 'S':
        for object in OBJECT_CONTAINER:
            if (object.x, object.y) in area_around_user and object.storage:
                object.storage.store(user)    
    
    if user_input == 'T':
        for object in OBJECT_CONTAINER:
            if (object.x, object.y) in area_around_user and object.storage:
                object.storage.query(user)

def player_toggle_door(user):
    area_around_user = [(dx + user.x, dy + user.y) for (dx, dy) in OFF_SETS]
    for object in OBJECT_CONTAINER:
        if (object.x, object.y) in area_around_user and object.door:
            object.door.toggle()

def player_travel_z(user, depth_index):
    user_inventory = user.creature.inventory
    for object in OBJECT_CONTAINER:
        print object.name
        if object != user and object.x == user.x and object.y == user.y and object.stairs:
            object.stairs.use_stairs(user, depth_index)
            save_infinity_chests()
            break
        
def player_equip_item(user):
    user_inventory = user.creature.inventory
    selected = check_inventory(user_inventory)
    
    if selected and selected.equipment:
        selected.equipment.toggle_equip(user)
        
def player_remove_item(user):
    user_attire = user.creature.attire
    selected = check_inventory(user_attire)
    
    if selected and selected.equipment:
        selected.equipment.toggle_equip(user)
        
def player_drop(user):
    user_inventory = user.creature.inventory
    selected = check_inventory(user_inventory)
    
    if selected:
        user_inventory.remove(selected)
        selected.item.drop(user.x, user.y)

def player_use_item(user):
    user_inventory = user.creature.inventory
    selected = check_inventory(user_inventory)
    
    # Selecting an equipment via USE function.
    if selected and selected.equipment:
        # user_inventory.remove(selected)
        selected.equipment.toggle_equip(user)
    
    if selected and selected.item.has_use:
        user_inventory.remove(selected)
        selected.item.use(user)

        
def player_pick_up(user):
    user_inventory = user.creature.inventory

    for object in OBJECT_CONTAINER:
        if object != user and object.x == user.x and object.y == user.y and object.item:
            user_inventory.append(object)
            object.item.pick_up()
            print 'Picked up {}.'.format(object.name)
            