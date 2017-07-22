from src.containers import *

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
        self.grid[10][10].make_wall()
        self.grid[10][9].make_wall()
        self.grid[9][9].make_wall()
        self.grid[10][11].make_wall()

        
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
