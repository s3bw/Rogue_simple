from src.map import Map
from src.objects import Object, Creature
from src.objects import creature_death
# from src.message import Message


moves = {'up': [-1,0],'down': [1,0],'left': [0,-1],'right': [0,1]}

all_objects = []

player = Creature(50, 5, creature_death)
user = Object(5, 5, 'Player Character', creature=player)
all_objects.append(user)

rabbit_creature = Creature(10, 0, creature_death)
rabbit = Object(3, 5, 'Rabbit', creature=rabbit_creature)
all_objects.append(rabbit)

bin = Object(7, 5, 'Bin')
all_objects.append(bin)

map = Map(10, 10)

def render_map():
    # global all_objects, map
    for object in all_objects:
        print (object.x, object.y)
        map.place_on_grid(object.x, object.y)
    map.show()
    print '-'*41
    
def player_move(user_input):
    dx, dy = moves[user_input]
    x = user.x + dx
    y = user.y + dy
    
    target = None
    for object in all_objects:
        if object.creature is not None and object.x == x and object.y ==y:
            print (object.creature is not None)
            target = object
            break
        
    print target
    if target is not None:
        print target.name
        user.creature.attack(target)
        
    else:
        user.move(map, dx, dy)
         
    
game_state = True
while game_state == True:
    render_map()
    user_input = raw_input('Where to?')
    if user_input == 'exit':
        break
    player_move(user_input)    



# print map.grid[5][5].blocked