import math
import random

from containers import *
from data.biome_types import BIOME_DATA

DEFAULT_GRID_X = 20
DEFAULT_GRID_Y = 20
MAX_ATTEMPTS = 20
MAX_SIZE_ROOM = 6 # wall external max 7, internal max 5
MIN_SIZE_ROOM = 3 # wall external min 4, internal min 2
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
    """ A Rectanglular polygon.
    
    :attributes:
        x1:     the most-left x co-ord
        y1:     the most-high y co-ord
        x2:     the most-right x co-ord
        y2:     the most-low y co-ord
        room:   the room component of the Rect
    """
    def __init__(self, building=None):
        h = self.rectangle_length()
        v = self.rectangle_length()
        
        max_x = DEFAULT_GRID_X - h - 1
        max_y = DEFAULT_GRID_Y - v - 1
    
        # Remeber the index starts at Zero: [0, 1, 2]
        x = random.randint(1, max_x-1)
        y = random.randint(1, max_y-1)
    
        self.x1 = x
        self.y1 = y
        self.x2 = x + h
        self.y2 = y + v

        self.building = building
        
        if self.building:
            self.building.owner = self
            
    def rectangle_length(self):
            """ Define the length of a rectangle side."""
            return random.randint(MIN_SIZE_ROOM, MAX_SIZE_ROOM)
        
    def build_element(self, new_value):
        doors = 2
        building_objects = 2
        if new_value > 20:
            doors = 1
            building_objects = 1
            
        #self.room.owner = self
        self.building = Building(value=new_value, doors=doors, immovable_objects=1, building_objects=building_objects)
        self.building.owner = self
        print 'Space Allocating'
        self.building.space_allocation()
        
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
        
    def structure_space(self, x, y, steps_away=0):
        _x1 = self.x1 - steps_away
        _y1 = self.y1 - steps_away
        _x2 = self.x2 + steps_away
        _y2 = self.y2 + steps_away
        
        return (_x1 <= x <= _x2 
            and _y1 <= y <= _y2)

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

"""
class River:
    def __init__(self):
        find point on bottom x axis,
        build towards top x axis,
        find point on y axis build bridge
"""

class Building:
    """ A Building object that encompasses all the features of this map structure
    
    :attributes:
        value
        doors
        building_objects
        immovable_objects
        internal_structure
        grid_space
        door_space
        internal_structure
        immovable_space
        object_space
        bin_space
    """
    
    def __init__(self, value=50, building_objects=None, doors=None, immovable_objects=None, internal_structure=None):
        self.value = value
        self.doors = doors
        self.building_objects = building_objects
        self.immovable_objects = immovable_objects
        self.internal_structure = internal_structure
        
        #Instead of h and v we need x and y - h and v is probably ok, double check consistency
        grid_h = range(DEFAULT_GRID_X)
        grid_v = range(DEFAULT_GRID_Y)
        self.grid_space = [(x, y) for x in grid_h for y in grid_v]

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
            
            internal_structure.remove(random.choice(internal_structure))
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
        self.object_space = self.allocate_spaces(object_space, self.building_objects)
        
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
        large_structures
        medium_structures
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
        
        self.biome = grid_biome
        self.first_grid = first_grid
        self.entry_point = entry_point
        self.create_grid()
        
        # Above ground grid needs an external space attribute


    def create_grid(self):
        self.grid = [[
            Tile(False)
            for x in range(self.grid_h)]
                for y in range(self.grid_v)
            ]

        self.determine_structure_sizes()
        self.allocate_structures()
        self.build_structural_elements()
        self.place_structures()
        self.externals()
        self.make_exit_point()
        
        
    def determine_structure_sizes(self):
        """ This function determines count of structures to be created inside the grid
        
        :attribute large_structures: (int) allocated large structures for the grid.
        :attribute medium_structures: (int) allocated medium structures for the grid.
        """
        self.large_structures = 0
        self.medium_structures = 4
    
        grid_value = random.randint(0,100)
        if grid_value > 80: # and not self.first_grid:
            self.large_structures = 1
            self.medium_structures = 2
            
        
    def allocate_structures(self):
        # Split grid_structures to make the placement before doing the internal gen.
        #   --> eg find a space on the map for all the objects
        #   --> make the objects more complex using allocated space
        ###self.biome_structures = BIOME_DATA[self.biome]
        
        self.structures = []
        
        completed_large_structures = 0
        while completed_large_structures < self.large_structures:
            new_structure = self.validate_structure('building', self.structures)

            if new_structure == False:
                self.structures = []
                completed_large_structures = 0
                print 'Map Rejected'
            
            else:
                completed_large_structures += 1
                self.structures.append(new_structure)
                
        completed_medium_structures = 0
        while completed_medium_structures < self.medium_structures:
            new_structure = self.validate_structure('building', self.structures)

            if new_structure == False:
                self.structures = []
                completed_medium_structures = 0
                print 'Map Rejected'
            
            else:
                completed_medium_structures += 1
                self.structures.append(new_structure)
                
        print self.structures

            
    def validate_structure(self, structure_type, structures):
        # Attempt to make a room in a spot allocating its size first,
        # This function can be 'place_structural_center(self, structure_type)'
        # If this fails move spot and try again
        # if this coninues to fail scrap the map and start again

        attempts = 0
        valid_structure = False
        while not valid_structure and MAX_ATTEMPTS >= attempts:
            if structure_type == 'building':
                map_object = Rect()

            # Define the valid structure
            if self.entry_point:
                # needs to be GENERAL, not all contain rectangle
                valid_structure = (not any(created_structure.intersect(map_object, steps_away=1) for created_structure in structures)) \
                    and all(not map_object.structure_space(x, y) for x, y in self.entry_point)
            else:
                valid_structure = not any(created_structure.intersect(map_object, steps_away=1) for created_structure in structures)
            attempts += 1
            
        if valid_structure:
            return map_object
            
        return False
        

    def build_structural_elements(self):
        new_value = random.randint(0,100)
        
        for map_object in self.structures:
            map_object.build_element(new_value)
                
        if self.first_grid:
            self.structures[0].building.users_start()
            

    def externals(self):
        grid = [(x, y) for y in range(self.grid_h) for x in range(self.grid_v)]
        for map_object in self.structures: 
            grid = [(x, y) for (x, y) in grid if not map_object.structure_space(x, y, 1)]
    
        self.external_area = grid
            
    def make_exit_point(self):
        selected_index = random.randint(1, len(self.external_area) - 1)
        self.exit_point = self.external_area[selected_index]


    def place_structures(self):
        for y in range(self.grid_h):
            for x in range(self.grid_v):
                for map_object in self.structures:

                    if map_object.building:
                        if map_object.building.internal_structure and (x, y) in map_object.building.internal_structure:
                            self.grid[x][y].make_wall()

                        elif map_object.edges(x,y) and (x,y) not in map_object.building.door_space:
                            self.grid[x][y].make_wall()
                    
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
