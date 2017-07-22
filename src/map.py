# '.' and '@' need to be changed to True and False when GUI is added.

class Tile:
    def __init__(self, portray='.', blocked=False):
        self.portray = portray
        self.blocked = blocked
        
class Map:
    def __init__(self, grid_h, grid_v, grid=None):
        self.grid_h = grid_h
        self.grid_v = grid_v
        self.grid = grid
        
        self.create_grid()
        
    def create_grid(self):
        self.grid = [[
            Tile()
            for y in range(self.grid_h)]
                for x in range(self.grid_v)
            ]

    def show(self, show_blocked=False):
        for grid_y in self.grid:
            print '| ' + ' | '.join([(
                tile.portray) 
                for tile in grid_y
            ]) + ' |'
            
        if show_blocked:
            for grid_y in self.grid:
                print '| ' + ' | '.join([(
                    str(tile.blocked)) 
                    for tile in grid_y
                ]) + ' |'
            
    def draw_on_grid(self, x, y, representation, passable):
        self.grid[x][y].portray = representation
        if not passable:
            self.grid[x][y].blocked = True
        
    def refresh_grid(self):
        for x in range(self.grid_h):
            for y in range(self.grid_v):
                self.grid[x][y].portray = '.'
                self.grid[x][y].blocked = False
        
    def is_blocked(self, x, y):
        return self.grid[x][y].blocked
            
        # for object in objects:
            # if object.blocks and object.x == x and object.y == y:
                # return True
                
        # return False
