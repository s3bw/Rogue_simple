# '.' and '@' need to be changed to True and False when GUI is added.

class Tile:
    def __init__(self, blocked='.'): #False):
        self.blocked = blocked
        
class Map:
    def __init__(self, grid_h, grid_v, grid=None):
        self.grid_h = grid_h
        self.grid_v = grid_v
        self.grid = grid
        
        self.create_grid()
        
    def create_grid(self):
        self.grid = [[
            Tile('.')
            for y in range(self.grid_h)]
                for x in range(self.grid_v)
            ]

    def show(self):
        for x in self.grid:
            print '| ' + ' | '.join([str(tile.blocked) for tile in x]) + ' |'
            
    def place_on_grid(self, x, y):
        if self.grid[x][y].blocked == '.':
            self.grid[x][y].blocked = '@'
        
    def remove_from_grid(self, x, y):
        if self.grid[x][y].blocked == '@':
            self.grid[x][y].blocked = '.'
        
        
    def is_blocked(self, x, y):
        if self.grid[x][y].blocked == '@':
            return True
            
        # for objects in objects:
            # if objects.blocks and object.x == x and object.y == y:
                # return True
                
        return False
