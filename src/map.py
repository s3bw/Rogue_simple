

class Tile:
    def __init__(self, blocked=False):
        self.blocked = blocked
        
class Map:
    def __init__(self, map_h, map_v):
        self.map_h = map_h
        self.map_v = map_v
        
    def create_map(self):
        map = [[
            Tile(False)
            for y in range(self.map_h)]
                for x in range(self.map_v)
            ]
