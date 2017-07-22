from src.map import Map
from src.containers import OBJECT_CONTAINER
from src.death_scenes import *
from src.item_uses import *
# from src.message import Message


class Object_Place:
    def __init__(self, 
            x, y, grid_level, name, representation, passable=False,
            creature=None,
            item=None
        ):
        
        self.x = x
        self.y = y
        self.grid_level = grid_level
        self.name = name
        self.representation = representation
        self.passable = passable
        
        self.creature = creature
        self.item = item
        
        if self.creature:
            self.creature.owner = self
        
        if self.item:
            self.item.owner = self
            self.passable = True
            
    def draw(self):
        self.grid_level.draw_on_grid(self.x, self.y, self.representation, self.passable)
            
    def send_to_back(self):
        OBJECT_CONTAINER.remove(self)
        OBJECT_CONTAINER.insert(0, self)
            
    def move(self, dx, dy):
        if not self.grid_level.is_blocked(self.x + dx, self.y + dy):
            self.x += dx
            self.y += dy

    
class Creature:
    def __init__(self, hp, power, death, inventory=None):
        self.max_hp = hp
        self.hp = hp
        self.power = power
        self.death = death
        self.inventory = inventory
        
    def take_damage(self, damage):
        if damage > 0:
            self.hp -= damage
            if self.hp <= 0:
                # Maybe drop the item here.
                # Item needs to be pickup-able, the corpse can't get in the way.
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
            
    def drop_item(self):
        highest_value = max(self.inventory, key=lambda x: x.item.value)
        self.inventory.remove(highest_value)
        highest_value.item.drop(self.owner.x, self.owner.y)
        
        print 'Dropped {}.'.format(highest_value.name)

class Item:
    def __init__(self, weight, value, intensity=0, has_use=None):
        self.weight = weight
        self.value = value
        self.intensity = intensity
        self.has_use = has_use
    
    def pick_up(self):
        OBJECT_CONTAINER.remove(self.owner)
    
    def drop(self, x, y):
        self.owner.x = x
        self.owner.y = y
        OBJECT_CONTAINER.append(self.owner)
        self.owner.send_to_back()
        
    def use(self, use_on):
        self.has_use(self, use_on.creature)

def creature_death(corpse):
    corpse.creature.drop_item()
    corpse.creature = None
    corpse.passable = True
    corpse.name = 'Mangled {} corpse.'.format(corpse.name)
    corpse.representation = '%'
    corpse.send_to_back()        

