import math
import random
from containers import *

MAX_SIZE_ROOM = 7
MIN_SIZE_ROOM = 4
ROOM_AREA = MAX_SIZE_ROOM * MAX_SIZE_ROOM
WALKING_AREA = 0.75

def room_length():
    return random.randint(MIN_SIZE_ROOM, MAX_SIZE_ROOM)

class Rect:
    def __init__(self, x, y, h, v, room=None):
        self.x1 = x
        self.y1 = y
        self.x2 = x + h
        self.y2 = y + v
        
        self.room = room
        
        if self.room:
            self.room.owner = self
        
    def center(self):
        center_x = (self.x1 + self.x2) / 2
        center_y = (self.y1 + self.y2) / 2
        return (center_x, center_y)
        
    def intersect(self, other):
        return (
            self.x1 <= other.x2 
            and self.x2 >= other.x1
            and self.y1 <= other.y2
            and self.y2 >= other.y1
        )
        
    def rectangle(self, x, y):
        return (self.x1 <= x <= self.x2 and self.y1 <= y <= self.y2)

    def internal(self, x, y):
        return (self.x1 < x < self.x2 and self.y1 < y < self.y2)
        
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
        
        object_space = [(x, y) for (x, y) in self.grid_space if self.owner.internal(x, y)]
        self.object_space = self.allocate_spaces(object_space, self.room_objects)
        del self.grid_space


        
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
    def __init__(self, grid_h, grid_v, grid_biome='village'):
        self.grid_h = grid_h
        self.grid_v = grid_v
        self.grid_area = self.grid_h * self.grid_v
        
        self.biome = grid_biome
        
        self.create_grid()
        
    def create_grid(self):
        self.grid = [[
            Tile(False)
            for x in range(self.grid_h)]
                for y in range(self.grid_v)
            ]

        calculate_space =  (self.grid_area*(1- WALKING_AREA)) / ROOM_AREA
        
        self.rooms = []
        space_for_rooms = calculate_space
        while space_for_rooms > 1:
            room_h = room_length()
            room_v = room_length()
            new_room = self.create_room(self.rooms, room_h, room_v)
            
            if new_room == False:
                print 'Map Rejected'
                self.rooms = []
                space_for_rooms = calculate_space
            
            else:
                space_for_rooms -= 1                
                self.rooms.append(new_room)
        
        for y in range(self.grid_h):
            for x in range(self.grid_v):
                if any(map_object.edges(x,y) and (x,y) not in map_object.room.door_space for map_object in self.rooms):
                    self.grid[x][y].make_wall()
                    
        # Include types of maps gen - above ground/below
            
    def create_room(self, rooms, new_h, new_v):
        max_x = self.grid_h - new_h - 1
        max_y = self.grid_v - new_v - 1
        
        attempts = 0
        valid_room = False
        while valid_room == False:
        
            attempts += 1
            if attempts == 20:
                return False
            
            new_x = random.randint(5, max_x)
            new_y = random.randint(5, max_y)
            
            new_value = random.randint(0,100)
            room_component = Room(self, value=new_value, doors=2, room_objects=2)
            map_object = Rect(new_x, new_y, new_h, new_v, room=room_component)
            
            # Valid room check
            if not any(created_room.intersect(map_object) for created_room in rooms):
                map_object.room.define_spaces()
                return map_object
                
        
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
