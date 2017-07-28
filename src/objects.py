from containers import OBJECT_CONTAINER
from death_scenes import *
from item_uses import *
from user_functions import check_inventory
# from src.message import Message


class Object_Place:
    def __init__(self, 
            x, y, grid_level, name, representation, passable=False,
            creature=None,
            item=None,
            equipment=None,
            door=None,
            storage=None
        ):
        
        self.x = x
        self.y = y
        self.grid_level = grid_level
        self.name = name
        self.representation = representation
        self.passable = passable
        
        self.creature = creature
        self.item = item
        self.equipment = equipment
        self.door = door
        
        if self.creature:
            self.creature.owner = self
        
        if self.equipment:
            self.equipment.owner = self
            self.passable = True
        
        if self.item:
            self.item.owner = self
            self.passable = True
            
        if self.door:
            self.door.owner = self            
            
    def draw(self):
        self.grid_level.draw_on_grid(self.x, self.y, self.representation, self.passable)
            
    def send_to_back(self):
        OBJECT_CONTAINER.remove(self)
        OBJECT_CONTAINER.insert(0, self)
            
    def move(self, dx, dy):
        if not self.grid_level.is_blocked(self.x + dx, self.y + dy):
            self.x += dx
            self.y += dy

            
class Door:
    # Need to see this to understand how many hits this takes (balance)
    def __init__(self, lock_strength=0.5, lock_durability=10, open=False):
        self.lock_durability = lock_durability
        self.lock_strength = lock_strength
        self.open = open
        
    def reduce_durability(self, damage):
        damage = damage * (1 - self.lock_strength)
        self.lock_durability -= int(damage)
        if self.lock_durability <= 0:
            self.open = True
            self.owner.passable = True
            self.owner.representation = '-'
            
    def toggle(self):
        if self.lock_durability <= 0:
            if self.open == False:
                print 'Openned'
                self.open = True
                self.owner.representation = '-'
                self.owner.passable = True
            else:
                print 'Closed'
                self.open = False
                self.owner.representation = '+'
                self.owner.passable = False
        else:
            print 'Door is locked.'
            
            
class Storage:
    def __init__(self, capacity, contains=None):
    # Storage object will become infinity chests - item save between plays
    # Once an item goes in it can only be taken out in other play through
        self.capacity = capacity
        self.contains = contains
        
    def query_storage(self, unit):
        units_inventory = unit.creature.inventory
        
        if not contains:
            print self.name, 'is empty.'
            return
        
        taking_item = check_inventory(self.contains)
        units_inventory.append(taking_item)
        
    def store(self, unit):
        units_inventory = unit.creature.inventory
        storing_item = check_inventory(units_inventory)
        
        units_inventory.remove(storing_item)
        self.contains.append(storing_item)
        

equip_bonus = lambda entity, attribute: sum(
    wearing_item.equipment.magnitute 
    for wearing_item in entity.attire 
    if wearing_item.equipment.affect == attribute
)
    
class Creature:
    def __init__(self, hp, power, death, inventory=None, attire=None):
        self.base_hp = hp
        self.hp = hp
        self.base_power = power
        
        self.death = death
        self.inventory = inventory
        self.attire = attire
        
    @property
    def power(self):
        if self.attire:
            return self.base_power + equip_bonus(self, 'power')
        return self.base_power
            
    @property
    def max_hp(self):
        if self.attire:
            return self.base_hp + equip_bonus(self, 'hp')
        return self.base_hp
        
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
        # include attire in this calculation currently only drops from inventory
        if self.inventory:
            highest_value = max(self.inventory, key=lambda x: x.item.value)
            self.inventory.remove(highest_value)
            highest_value.item.drop(self.owner.x, self.owner.y)
        
            print 'Dropped {}.'.format(highest_value.name)
        
    def is_slot_empty(self, check_slot):
        for item_in_bag in self.attire:
            if check_slot == item_in_bag.equipment.slot:
                return item_in_bag

        
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
        if self.has_use is not None:
            self.has_use(self, use_on.creature)

        
class Equipment:
    def __init__(self, slot, magnitute, affect=None):
        self.slot = slot
        self.is_equipped = False
        
        self.magnitute = magnitute
        self.affect = affect        
                    
        # if object is in attire when generating the game it gets equiped value False.
        # This is not the case as it's in a creatures attire 

        all_attire = [entity.creature.attire for entity in OBJECT_CONTAINER if entity.creature]
        if self not in OBJECT_CONTAINER and (self in all_attire):
            self.is_equipped = True
        
    # @property
    # def is_equipped(self):
        # return self._is_equipped
        
    # @is_equipped.setter
    # def is_equipped(self):
        # global_attire = [
            # dressed.creature.attire 
            # for dressed in OBJECT_CONTAINER 
            # if dressed.creature is not None
        # ]
        
        # self._is_equipped = (self in global_attire)
        
#        if self in global_attire:
  #          self.is_equipped = True
        
        
    def toggle_equip(self, unit):
        print self.owner.name, 'equipt?', self.is_equipped
        if self.is_equipped:
            self.dequip(unit.creature)
        else:
            self.equip(unit.creature)
            
    def equip(self, creature):
        equipment_in_slot = creature.is_slot_empty(self.slot)
        if equipment_in_slot:
            equipment_in_slot.equipment.dequip(creature)
            
        self.is_equipped = True
        creature.inventory.remove(self.owner)
        creature.attire.append(self.owner)
        print 'Now wearing {}.'.format(self.owner.name)
        
    def dequip(self, creature):        
        if not self.is_equipped:
            return
        self.is_equipped = False
        creature.attire.remove(self.owner)
        creature.inventory.append(self.owner)
        print 'Taken {} off.'.format(self.owner.name)
        

def creature_death(corpse):
    corpse.creature.drop_item()
    corpse.creature = None
    corpse.passable = True
    corpse.name = 'Mangled {} corpse.'.format(corpse.name)
    corpse.representation = '%'
    corpse.send_to_back()        
