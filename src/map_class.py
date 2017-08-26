import math
import random

from containers import *
from data.biome_types import BIOME_DATA

DEFAULT_GRID_X = 20
DEFAULT_GRID_Y = 20
MAX_ATTEMPTS = 20
MAX_SIZE_ROOM = 6 # wall external max 7, internal max 5
MIN_SIZE_ROOM = 3 # wall external min 4, internal min 2
# Rooms with internal structures:
#   5x5, 5x4
ROOM_AREA = MAX_SIZE_ROOM * MAX_SIZE_ROOM
WALKING_AREA = 0.70

OFFSETS = [(0, 1),(0, -1),(1, 0),(-1, 0)]
DIAGONAL_OFFSETS = [(-1, -1),(1, -1),(1, 1),(-1, 1)]


    
    
def trim_list(the_list, value, other_list):
    """ Given an ordered range and a number in that range.
    Split the list in two at the index of that value and return the larger of the resulting lists.
    
    :param the_list: (list) of a range to be split into two lists. (e.g [ 2, 3, 4, 5])
    :param value: (int) the value to split the list at. (e.g. 3)
    :return: The large side after split. (e.g. [4, 5])
    """
    index = the_list.index(value)
    
    other_list = other_list[1:-1]
    
    left_side = the_list[:index]
    right_side = the_list[index+1:]    
    if len(left_side) == len(right_side):
        return left_side[1:] + right_side[:-1], other_list
        
    elif len(left_side) > len(right_side):
        return left_side[1:], other_list
    return right_side[:-1], other_list
    

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
    def __init__(self, grid, value=0, room_objects=None, doors=None, immovable_objects=None, internal_structure=None):
        self.value = value
        self.doors = doors
        self.room_objects = room_objects
        self.immovable_objects = immovable_objects
        self.internal_structure = internal_structure
        
        #Instead of h and v we need x and y - h and v is probably ok, double check consistency
        grid_h = range(grid.grid_h)
        grid_v = range(grid.grid_v)
        self.grid_space = [(x, y) for x in grid_h for y in grid_v]
        
        if value > 20:
            self.doors = 1
            self.room_objects = 1
            
    def allocate_spaces(self, space, number_to_select):
        """Out of a list of co-ordinates this function chooses (int) 'number_to_select' co-ordinates."""
        if len(space) < number_to_select:
            number_to_select = len(space)
        return random.sample(space, number_to_select)
        
    def door_places(self):        
        door_space = [(x, y) for (x, y) in self.grid_space if self.owner.sides(x, y)]
        self.door_space = self.allocate_spaces(door_space, self.doors)
        
    def internal_places(self):
        h = self.owner.x2 - self.owner.x1 - 1
        v = self.owner.y2 - self.owner.y1 - 1
        
        area = h * v
        door_space = self.door_space        
        if area > 15 and len(door_space) == 1:
            # Plot interior area
            ix1 = self.owner.x1 + 1
            ix2 = self.owner.x2 
            iy1 = self.owner.y1 + 1
            iy2 = self.owner.y2

            ih = range(ix1, ix2)
            iv = range(iy1, iy2)
            
            # Remove structures away from door and sides
            door_x, door_y = door_space[0]
            if door_x in ih:
                ih, iv = trim_list(ih, door_x, iv)
            else:
                iv, ih = trim_list(iv, door_y, ih)
                
            # Choose structure direction, then make a passable gap
            verticle_line = bool(random.getrandbits(1))
            if verticle_line:
                ih = random.choice(ih)
                internal_structure = [(ih, y) for y in range(iy1, iy2)]
            else:
                iv = random.choice(iv)
                internal_structure = [(x, iv) for x in range(ix1, ix2)]
            
            print len(internal_structure)
            internal_structure.remove(random.choice(internal_structure))
            print len(internal_structure)
            self.internal_structure = internal_structure

    def clear_doorway(self, internal_space):
        """ Remove all doorways from object space.
        
        :param internal_space: (list) containing co-ordinates of all internal points.
        :return: The 'internal_space' without doorways.
        """
        for main_door_x, main_door_y in self.door_space:
            door_way = [(main_door_x + dx, main_door_y + dy) for dx, dy in OFFSETS]
            internal_space = [(x, y) for x, y in internal_space if (x, y) not in door_way]
            
        return internal_space
        
    def immovable_places(self):
        """ This should consist of the corners, with the exception of some cases"""
        top_left = (self.owner.x1 + 1, self.owner.y1 + 1)
        top_right = (self.owner.x2 - 1, self.owner.y1 + 1)
        bottom_left = (self.owner.x1 + 1, self.owner.y2 - 1)
        bottom_right = (self.owner.x2 - 1, self.owner.y2 - 1)
        immovable_places = [top_left, top_right, bottom_left, bottom_right]
        immovable_places = self.clear_doorway(immovable_places)
        
        select_immovable_places = []
        for corner_x, corner_y in immovable_places:
            corner = (corner_x, corner_y)
        
            adjacent = [(corner_x + dx, corner_y + dy) for (dx, dy) in OFFSETS]
            diagonal_adjacent = [(corner_x + dx, corner_y + dy) for (dx, dy) in DIAGONAL_OFFSETS]
            
            if self.internal_structure is not None:
                adjacent = [place for place in adjacent if place in self.internal_structure]
                diagonal_adjacent = [place for place in diagonal_adjacent if place in self.internal_structure]
                
                if len(diagonal_adjacent) == 1 and len(adjacent) != len(diagonal_adjacent):
                    continue
                else:
                    select_immovable_places.append(corner)
            else:
                select_immovable_places.append(corner)
        
        self.immovable_space = self.allocate_spaces(select_immovable_places, self.immovable_objects)
        
    def object_places(self):
        object_space = [(x, y) for (x, y) in self.grid_space if self.owner.internal(x, y) and (x, y) != self.owner.center() and ((x, y) not in self.immovable_space)]
        if self.internal_structure is not None:
            object_space = [(x, y) for (x, y) in object_space if (x, y) not in self.internal_structure]
        
        object_space = self.clear_doorway(object_space)
        self.object_space = self.allocate_spaces(object_space, self.room_objects)
        
    def space_allocation(self):
        self.door_places()
        self.internal_places()
        self.immovable_places()
        self.object_places()
        del self.grid_space
        
    def users_start(self):
        self.user_space = self.object_space[0]
        self.door_space = self.door_space[:1]
        self.bin_space = self.immovable_space[0]
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
        
    def make_river(self):
        self.wall_tile = False
        self.blocked = True
        self.portray = 'w'
        
    def make_bridge(self):
        self.wall_tile = False
        self.blocked = False
        self.portray = '='

        # when I move to gui this will become important
        # self.block_sight = True
        
        
class Grid:
    """ The area that the player can move around in and interact with.
    :Attribute:
        grid_h                  (int) the height of the grid
        grid_v                  (int) the verticle of the grid
        grid_z                  (int) the z/depth level of the grid
        grid_value              (int) the value of the grid defines what things can spawn
        biome                   (string) the type of grid to be generated
        first_grid              (bool) identifying the first grid generated #CHANGES - make int first - this can be the z level
        entry_point             (list) of tuple, containing co-ords of places that cant be built upon
        exit_point              (tuple) co-ords of a point of exit
        structures              (list) of room structures on the grid
            - rooms can be changes to structures containing not only rooms
        grid                    (list) of tuples containing all co-ords making up the grid
        --> should contain var that has buildable space
    """
    def __init__(self, grid_h=DEFAULT_GRID_X, grid_v=DEFAULT_GRID_Y, grid_z=0, grid_biome='village', first_grid=False, entry_point=None):
        self.grid_h = grid_h
        self.grid_v = grid_v
        self.grid_z = grid_z
        
        self.grid_value = random.randint(0,100)
        self.biome = grid_biome
        self.first_grid = first_grid
        self.entry_point = entry_point
        self.create_grid()
        """
        Separate the map obejcts from the map
            Create the variable 'map_objects' to contain all objects and types.
            
            On creating the map append and search this space for possible locations.
            
            Build objects in free space by passing the grid into the objects (like 'house') structure or 'tree' structure
            
            House object should decide on the object type - depending on the space it receives
            
            have attempts to pick a space and a size. 
            
            gen with params 'small' 'med' and 'large'
        
        
        """
        
        # Above ground grid needs an external space attribute
            
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
        # Instead:
        # allocate_structures()
        # place_structural_elements()
        # make_exit_point()
        self.allocate_structures()
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

    def place_stuctural_elements(self):
        for map_object in self.structures:
            map_object.room.space_allocation()

    def allocate_structures(self):
        # Split grid_structures to make the placement before doing the internal gen.
        #   --> eg find a space on the map for all the objects
        #   --> make the objects more complex using allocated space
        self.biome_structures = BIOME_DATA[self.biome]
        
        grid_area = self.grid_h * self.grid_v
        calculate_space =  (grid_area*(1- WALKING_AREA)) / ROOM_AREA
        
        self.structures = []
        available_area = calculate_space
        print available_area
        while available_area > 1:
            # Larger structures are rare
            #if self.grid_value > 80:
            new_structure = self.create_structure('river', self.structures)
                
            
        
            #new_structure = self.create_room(self.structures)
            
            if new_structure == False:
                self.structures = []
                available_area = calculate_space
                print 'Map Rejected'
            
            else:
                available_area -= new_structure.size
                self.structures.append(new_structure)
                
        if self.first_grid:
            # this wont work if the first structure is not a room
            self.structures[0].room.users_start()
            
    def create_room(self, rooms):
        # Attempt to make a room in a spot allocating its size first,
        # This function can be 'place_structural_center(self, structure_type)'
        # If this fails move spot and try again
        # if this coninues to fail scrap the map and start again
        
        def room_length(): ###
            """ Define the length  of a room side."""
            return random.randint(MIN_SIZE_ROOM, MAX_SIZE_ROOM) ###
            
        grid_max_x = lambda length: self.grid_h - length - 1 # 
        grid_max_y = lambda length: self.grid_v - length - 1
        
        attempts = 0
        valid_room = False
        while not valid_room and MAX_ATTEMPTS >= attempts:
            # cut the shapes in the room object
            new_h = room_length()
            new_v = room_length()
            
            max_x = grid_max_x(new_h)
            max_y = grid_max_y(new_v)
            new_value = random.randint(0,100)
            
            # Remeber the index starts at Zero: [0, 1, 2]
            new_x = random.randint(1, max_x-1)
            new_y = random.randint(1, max_y-1)
            
            # if room has two doors on different edges try build an extention.
            room_component = Room(grid=self, value=new_value, doors=2, immovable_objects=1, room_objects=2)
            map_object = Rect(new_x, new_y, new_h, new_v, room=room_component)
            
            if self.entry_point:
                valid_room = (not any(created_room.intersect(map_object, steps_away=1) for created_room in rooms)) \
                    and all(not map_object.rectangle(x, y) for x, y in self.entry_point)
            else:
                valid_room = not any(created_room.intersect(map_object, steps_away=1) for created_room in rooms)
            attempts += 1
            
        if valid_structure:
            return map_object
            
        return False

    def place_walls(self):
        for y in range(self.grid_h):
            for x in range(self.grid_v):
                for map_object in self.structure:
                    # Build Rooms
                    if map_object.room:
                        # Room with internal Walls
                        if map_object.room.internal_structure and (x, y) in map_object.room.internal_structure:
                            self.grid[x][y].make_wall()
                            #self.grid[x][y].blocked = True
                            
                        # Room without internal walls
                        elif map_object.edges(x,y) and (x,y) not in map_object.room.door_space:
                            self.grid[x][y].make_wall()
                            #self.grid[x][y].blocked = True
                    
                    elif map_object.river:
                        if (x, y) in map_object.river.space:
                            self.grid[x][y].make_river()
                            
                    elif map_object.bridge:
                        if (x, y) in map_object.bridge.space:
                            self.grid[x][y].make_bridge()
                    
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
