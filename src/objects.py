from src.map import Map


class Object:
    def __init__(self, x, y, name, creature=None):
        self.x = x
        self.y = y
        self.name = name
        self.creature = creature
        
        if self.creature:
            self.creature.owner = self
            
    def move(self, grid, dx, dy):
        if not grid.is_blocked(self.x + dx, self.y + dy):
            self.x += dx
            self.y += dy
        
    
class Creature:
    def __init__(self, hp):
        self.hp = hp


