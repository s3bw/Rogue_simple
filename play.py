from src.map import Map
from src.objects import Object_Place, Creature
from src.objects import creature_death
# from src.message import Message


moves = {'up': [-1,0],'down': [1,0],'left': [0,-1],'right': [0,1]}

map = Map(10, 10)

all_objects = []

player = Creature(50, 5, creature_death)
user = Object_Place(5, 5, map, 'Player Character', '@', creature=player)
all_objects.append(user)

rabbit_creature = Creature(10, 0, creature_death)
rabbit = Object_Place(3, 5, map, 'Rabbit', 'r', creature=rabbit_creature)
all_objects.append(rabbit)

bin = Object_Place(7, 5, map, 'Bin', 'b')
all_objects.append(bin)



def render_map():
    map.refresh_grid()
    for object in all_objects:
        if object != user:
            object.draw()    
    
        print (object.x, object.y)
        
    user.draw()
    map.show()
    print '-'*41

    
def player_move(user_input):
    dx, dy = moves[user_input]
    x = user.x + dx
    y = user.y + dy
    
    target = None
    for object in all_objects:
        if object.creature is not None and object.x == x and object.y ==y:
            target = object
            break
        
    if target is not None:
        user.creature.attack(target)
        
    else:
        user.move(dx, dy)
         
    
game_state = True
while game_state == True:
    render_map()
    
    user_input = raw_input('Where to?')
    if user_input == 'exit':
        break
        
    if user_input in moves:
        player_move(user_input)    



# print map.grid[5][5].blocked