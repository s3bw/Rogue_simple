from src.map import Map
from src.containers import OBJECT_CONTAINER
from src.death_scenes import *
from src.item_uses import *
# from src.message import Message


class Object_Place:
    def __init__(self, 
            x, y, grid_level, name, representation, passable=False,
            creature=None,
            item=None,
            equipment=None
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
        
        if self.creature:
            self.creature.owner = self
        
        if self.equipment:
            self.equipment.owner = self
            self.passable = True
        
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
            bonus = sum(
                wearing_item.equipment.magnitute 
                for wearing_item in self.attire if wearing_item.equipment.affect == 'power'
            )
            return self.base_power + bonus
        return self.base_power
            
    @property
    def max_hp(self):
        if self.attire:
            bonus = sum(
                wearing_item.equipment.magnitute 
                for wearing_item in self.attire if wearing_item.equipment.affect == 'hp'
            )
            return self.base_hp + bonus
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
        # include attire in this calculation
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
        
    def toggle_equip(self, unit):
        if self.is_equipped:
            self.dequip(unit.creature)
        else:
            self.equip(unit.creature)
            
    def equip(self, creature):
        equipment_already_in_slot = creature.is_slot_empty(self.slot)
        if equipment_already_in_slot:
            equipment_already_in_slot.dequip(creature)
            
        self.is_equipped = True
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

