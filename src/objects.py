from src.map import Map
# from src.message import Message


class Object_Place:
    def __init__(self, x, y, grid_level, name, representation, passable=False, creature=None):
        self.x = x
        self.y = y
        self.grid_level = grid_level
        self.name = name
        self.representation = representation
        
        self.passable = passable
        self.creature = creature
        
        if self.creature:
            self.creature.owner = self
            
    def draw(self):
        self.grid_level.draw_on_grid(self.x, self.y, self.representation, self.passable)
            
    # def send_to_back(self, object_list):
        # object_list.remove(self)
        # object_list.insert(0, self)
        # return object_list
            
    def move(self, dx, dy):
        if not self.grid_level.is_blocked(self.x + dx, self.y + dy):
            self.x += dx
            self.y += dy

        
    
class Creature:
    def __init__(self, hp, power, death):
        self.hp = hp
        self.power = power
        self.death = death
        
    def take_damage(self, damage):
        if damage > 0:
            self.hp -= damage
            if self.hp <= 0:
                print '{} has Died.'.format(self.owner.name)
                self.death(self.owner)
            else:
                print '{} has {} remaining HP.'.format(self.owner.name, self.hp)

    def attack(self, target):
        damage = self.power
        if damage > 0:
            attacker = self.owner
            print '{} has hit {} with {} worth of damage!'.format(attacker.name, target.name, damage)        
            
            target.creature.take_damage(damage)

        # Message.attack_message(attacker, target, damage, outcome)
            
def creature_death(corpse):
    corpse.creature = None
    corpse.passable = True
    corpse.name = 'Mangled {} corpse.'.format(corpse.name)
    corpse.representation = '%'

