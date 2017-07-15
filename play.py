from src.map import Map
from src.objects import Object, Creature


moves = {'up': [-1,0],'down': [1,0],'left': [0,-1],'right': [0,1]}

all_objects = []

player = Creature(50)
user = Object(5, 5, 'Player Character', creature=player)
all_objects.append(user)

map = Map(10, 10)

def render_map():
    global all_objects, map
    for object in all_objects:
        map.place_on_grid(object.x, object.y)
    map.show()
    print '-'*41

    

render_map()
user_input = raw_input('Where to?')
while user_input != 'exit':
    try:
        dx, dy = moves[user_input]
        user.move(map, dx, dy)
    except:
        print 'Incorrect move!'
        
    render_map()
    print all_objects
    
    user_input = raw_input('Where to?')



# print map.grid[5][5].blocked