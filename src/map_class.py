import math
import random
from containers import *

DEFAULT_GRID_X = 20
DEFAULT_GRID_Y = 20
MAX_ATTEMPTS = 20
MAX_SIZE_ROOM = 6
MIN_SIZE_ROOM = 3
ROOM_AREA = MAX_SIZE_ROOM * MAX_SIZE_ROOM
WALKING_AREA = 0.70

def room_length():
    return random.randint(MIN_SIZE_ROOM, MAX_SIZE_ROOM)

class Rect:
    def __init__(self, x, y, h, v, room=None):
        self.x1 = x
        self.y1 = y
        self.x2 = x + h
        self.y2 = y + v
        
        #Look into compartmentalising large rooms
        #Look into slightly roundifying rooms on length of edges
        #   -------          --------
        #   |     |          |      |
        #   |     |  -->    /        \
        #   |     |  -->   |          |
        #   |     |  -->   |          |
        #   |     |  -->    \        /
        #   |     |          |      |
        #   -------          --------
        self.area = h * v
                
        self.room = room
        
        if self.room:
            self.room.owner = self
        
    def center(self):
        center_x = (self.x1 + self.x2) / 2
        center_y = (self.y1 + self.y2) / 2
        return (center_x, center_y)
        
    def intersect(self, other, steps_away=0):
        other_x1 = other.x1 - steps_away
        other_y1 = other.y1 - steps_away
        other_x2 = other.x2 + steps_away
        other_y2 = other.y2 + steps_away
        
        return (self.x1 <= other_x2
            and self.y1 <= other_y2
            and self.x2 >= other_x1
            and self.y2 >= other_y1)
        
    def rectangle(self, x, y):
        return (self.x1 <= x <= self.x2 and self.y1 <= y <= self.y2)

    def internal(self, x, y):
        return (self.x1 < x < self.x2 and self.y1 < y < self.y2)
        
    # Look into simplifiying these two below
    def edges(self, x, y):
        return (self.x1 == x and self.y1 <= y <= self.y2) \
            or (self.x2 == x and self.y1 <= y <= self.y2) \
            or (self.y1 == y and self.x1 <= x <= self.x2) \
            or (self.y2 == y and self.x1 <= x <= self.x2)
            
    def sides(self, x, y):
        return (self.x1 == x and self.y1 < y < self.y2) \
            or (self.x2 == x and self.y1 < y < self.y2) \
            or (self.y1 == y and self.x1 < x < self.x2) \
            or (self.y2 == y and self.x1 < x < self.x2)

        
class Room:
    def __init__(self, grid, value=0, room_objects=None, doors=None):
        self.value = value
        self.doors = doors
        self.room_objects = room_objects
        
        #Instead of h and v we need x and y - h and v is probably ok, double check consistency
        grid_h = range(grid.grid_h)
        grid_v = range(grid.grid_v)
        self.grid_space = [ (x, y) for x in grid_h for y in grid_v]
        
        if value > 50:
            self.doors = 1
            self.room_objects = 1
            
    def allocate_spaces(self, space, allocate_item):
        potential_spaces = len(space) - 1
        space_index = [random.randint(1, potential_spaces) for n in range(allocate_item)]
        return [space[index] for index in space_index]
        
    def define_spaces(self):        
        door_space = [(x, y) for (x, y) in self.grid_space if self.owner.sides(x, y)]
        self.door_space = self.allocate_spaces(door_space, self.doors)
        
        object_space = [(x, y) for (x, y) in self.grid_space if self.owner.internal(x, y) and (x, y) != self.owner.center()]
        self.object_space = self.allocate_spaces(object_space, self.room_objects)
        del self.grid_space
        
    def users_start(self):
        self.user_space = self.owner.center()
        print self.door_space[0]
        self.door_space = self.door_space[:1]
        #place bin on far side
        #make bin away from door
        self.bin_space = self.object_space[0]
        self.object_space = []

        
class Tile:
    def __init__(self, wall_tile, portray='.', blocked=False):    
        self.portray = portray
        self.blocked = blocked
        self.wall_tile = wall_tile
                
    def make_wall(self):
        self.wall_tile = True
        self.blocked = True
        self.portray = '#'

        # when I move to gui this will become important
        # self.block_sight = True
        
        
class Grid:
    def __init__(self, grid_h=DEFAULT_GRID_X, grid_v=DEFAULT_GRID_Y, grid_z=0, grid_biome='village', first_grid=False):
        self.grid_h = grid_h
        self.grid_v = grid_v
        self.grid_z = grid_z
        self.grid_area = self.grid_h * self.grid_v
        
        self.biome = grid_biome
        self.first_grid = first_grid
        self.create_grid()
        
            
        # Space allocation
        # --> Some kinda random_noise to make random outside objects,
        # --> Invert the room to make caverns
        # --> Tunnel space
        # --> Think about slightly differing tile colours
            
            
    def create_grid(self):
        self.grid = [[
            Tile(False)
            for x in range(self.grid_h)]
                for y in range(self.grid_v)
            ]

        self.allocate_room_space()
        self.place_walls()
        self.allocate_exit()
        
    def allocate_exit(self):
        possible_space = []
        for y in range(self.grid_h):
            for x in range(self.grid_v):
                if not self.grid[x][y].blocked:
                    possible_space.append((x, y))    
        
        selected_index = random.randint(1, len(possible_space) - 1)
        
        self.exit_point = possible_space[selected_index]
        
        
    def allocate_room_space(self):
        calculate_space =  (self.grid_area*(1- WALKING_AREA)) / ROOM_AREA
        
        self.rooms = []
        space_for_rooms = calculate_space
        while space_for_rooms > 1:
            new_room = self.create_room(self.rooms)
            
            if new_room == False:
                self.rooms = []
                space_for_rooms = calculate_space
                print 'Map Rejected'
            
            else:
                space_for_rooms -= 1
                self.rooms.append(new_room)
                
        if self.first_grid:
            self.rooms[0].room.users_start()
            
    def create_room(self, rooms):
        grid_max_x = lambda length: self.grid_h - length - 1
        grid_max_y = lambda length: self.grid_v - length - 1
        
        attempts = 0
        valid_room = False
        while valid_room == False and MAX_ATTEMPTS >= attempts:
            new_h = room_length()
            new_v = room_length()
            max_x = grid_max_x(new_h)
            max_y = grid_max_y(new_v)
            new_value = random.randint(0,100)
            new_x = random.randint(1, max_x-1)
            new_y = random.randint(1, max_y-1)
            
            room_component = Room(grid=self, value=new_value, doors=2, room_objects=2)
            map_object = Rect(new_x, new_y, new_h, new_v, room=room_component)
            
            valid_room = not any(created_room.intersect(map_object, steps_away=1) for created_room in rooms)
            attempts += 1
            
        if valid_room:
            map_object.room.define_spaces()
            return map_object
            
        return False

    def place_walls(self):
        for y in range(self.grid_h):
            for x in range(self.grid_v):
                if any(map_object.edges(x,y) and (x,y) not in map_object.room.door_space for map_object in self.rooms):
                    self.grid[x][y].make_wall()
                    self.grid[x][y].blocked = True
                    
        # Include types of maps gen - above ground/below
        
    def show(self):
        for grid_y in self.grid:
            print '| ' + ' | '.join([(
                tile.portray) 
                for tile in grid_y
            ]) + ' |'
            
            
    def draw_on_grid(self, x, y, representation, passable):
        self.grid[x][y].portray = representation
        if passable == False:
            self.grid[x][y].blocked = True
        else:
            self.grid[x][y].blocked = False
        
    def refresh_grid(self):
        objects_on_grid = [(object.x, object.y) for object in OBJECT_CONTAINER if not object.passable]

        for x in range(self.grid_h):
            for y in range(self.grid_v):
                if (x, y) not in objects_on_grid and self.grid[x][y].wall_tile == False:
                    self.grid[x][y].portray = '.'
                    self.grid[x][y].blocked = False
        
    def is_blocked(self, x, y):
        return self.grid[x][y].blocked
            
        # for object in objects:
            # if object.blocks and object.x == x and object.y == y:
                # return True
                
        # return False
