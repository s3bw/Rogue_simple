import math
import random
from src.containers import *

MAX_SIZE_ROOM = 7
MIN_SIZE_ROOM = 4
ROOM_AREA = MAX_SIZE_ROOM * MAX_SIZE_ROOM
WALKING_AREA = 0.75

class Rect:
    def __init__(self, x, y, w, h):
        self.x1 = x
        self.y1 = y
        self.x2 = x + w
        self.y2 = y + h
        
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
        
    def is_in_rectangle(self, place_x, place_y):
        return (self.x1 <= place_x <= self.x2 and self.y1 <= place_y <= self.y2)

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

        
class Map:
    def __init__(self, grid_h, grid_v, grid=None):
        self.grid_h = grid_h
        self.grid_v = grid_v
        self.grid = grid
        
        self.create_grid()
        
    def create_grid(self):
        self.grid = [[
            Tile(False)
            for y in range(self.grid_h)]
                for x in range(self.grid_v)
            ]

        self.grid_area = self.grid_h * self.grid_v        
        rooms = []        
        space_for_rooms = (self.grid_area*(1- WALKING_AREA)) / ROOM_AREA
        while space_for_rooms > 1:
            print space_for_rooms
            
            room_w = random.randint(MIN_SIZE_ROOM,MAX_SIZE_ROOM)
            room_h = random.randint(MIN_SIZE_ROOM,MAX_SIZE_ROOM)
            print (room_w, room_h)
            room = self.create_room(rooms, room_w, room_h)
            rooms.append(room)
            space_for_rooms -= 1
        
        for y in range(self.grid_h):
            for x in range(self.grid_v):
                if any(room.is_in_rectangle(x,y) for room in rooms):
                    self.grid[x][y].make_wall()
            

    def create_room(self, rooms, w, h):
        place_room = False
        while place_room == False:
            new_x = random.randint(5, self.grid_h - w)
            new_y = random.randint(5, self.grid_v - h)
            room = Rect(new_x, new_y, w, h)
            if not any(created_room.intersect(room) for created_room in rooms):
                return room
        
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
        print objects_on_grid
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
