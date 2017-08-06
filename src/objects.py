import shelve
import random

import generate_map as map_gen
from containers import OBJECT_CONTAINER, WORLD_CONTAINER
from death_scenes import *
from item_uses import *
from user_functions import check_inventory
# from src.message import Message

INFINITY_DATA = './src/infinity_data/'

class Object_Place:
    def __init__(self, 
            x, y, active_z, name, representation, passable=False,
            creature=None,
            item=None,
            equipment=None,
            door=None,
            storage=None,
            stairs=None
        ):
        
        self.x = x
        self.y = y
        self.active_z = active_z
        self.name = name
        self.representation = representation
        self.passable = passable
        
        self.creature = creature
        self.item = item
        self.equipment = equipment
        self.door = door
        self.storage = storage
        self.stairs = stairs
        
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
            
        if self.storage:
            self.storage.owner = self
            
        if self.stairs:
            self.stairs.owner = self
            self.passable = True
          
    @property
    def grid_level(self):
        return WORLD_CONTAINER[0]
            
    def draw(self):
        self.grid_level.draw_on_grid(self.x, self.y, self.representation, self.passable)
            
    def send_to_back(self):
        OBJECT_CONTAINER.remove(self)
        OBJECT_CONTAINER.insert(0, self)
            
    def move(self, dx, dy):
        if not self.grid_level.is_blocked(self.x + dx, self.y + dy):
            self.x += dx
            self.y += dy


class Stairs:
    def __init__(self, go_down=True):
        # '<' up stair, '>' down stair.
        self.go_down = go_down
        
        
    def use_stairs(self, unit, depth_index):
        depth_index = depth_index + 1 if self.go_down else depth_index - 1
        
        OBJECT_CONTAINER.remove(unit)
        del OBJECT_CONTAINER[:]
        del WORLD_CONTAINER[:]
        OBJECT_CONTAINER.append(unit)

        map_gen.generate(depth_index, self.go_down)
        unit.active_z = depth_index
    
    
class Door:
    # Need to see this to understand how many hits this takes (balance)
    def __init__(self, lock_strength=0.5, lock_durability=10, open=False):
        self.lock_durability = lock_durability
        self.lock_strength = lock_strength
        self.open = open
        
    def reduce_durability(self, damage):
        damage = float(damage) * (1 - self.lock_strength)
        # door strength should be exponential.
        # after one hit a suggestion of how long
        # it will take to get in should appear
        self.lock_durability -= damage
        if self.lock_durability <= 0:
            self.open = True
            self.owner.passable = True
            self.owner.representation = '-'
            
    def toggle(self): #separate
        if self.lock_durability <= 0:
            self.try_use()
        else:
            print 'Door is locked.'
            
    def try_use(self):
        if self.open == False:
            self.open = True
            self.owner.passable = True
            self.owner.representation = '-'
            print 'Openned'
        else:
            self.close_door()
            
    def close_door(self):
        self.open = False
        self.owner.passable = False
        self.owner.representation = '+'
        print 'Closed'
            
            
class Storage:
    # Storage object will become infinity chests - item save between plays
    # Once an item goes in it can only be taken out in other play through
    def __init__(self, capacity, contains=None, infinity_id=None, is_infinity=False):
        self.max_capacity = capacity
        self.contains = contains
        self.infinity_id = infinity_id
        self.is_infinity = is_infinity
        
        if is_infinity:
            try:
                infinity_data = shelve.open('{}game_save.txt'.format(INFINITY_DATA))
                self.contains = infinity_data[self.infinity_id]
                infinity_data.close()
            except:
                self.contains = contains

    @property
    def remaining_capacity(self):
        used_capacity = sum(stored_item.item.weight for stored_item in self.contains)
        return self.max_capacity - used_capacity
        
    def query(self, unit):
        units_inventory = unit.creature.inventory
        if not self.contains:
            print self.owner.name, 'is empty.'
            return
        
        # checking inventory might go into utils, this will need to become number and not string selection
        taking_item = check_inventory(self.contains)
        self.contains.remove(taking_item)
        units_inventory.append(taking_item)
        
    def store(self, unit):
        units_inventory = unit.creature.inventory
        storing_item = check_inventory(units_inventory)

        if storing_item and self.remaining_capacity > storing_item.item.weight:
            units_inventory.remove(storing_item)
            self.contains.append(storing_item)
            
        elif storing_item:
            print "Can't fit {} in {}.".format(storing_item.name, self.owner.name)
        

equip_bonus = lambda entity, attribute: sum(
    wearing_item.equipment.magnitute 
    for wearing_item in entity.attire 
    if wearing_item.equipment.affect_attribute == attribute
)
    
class Creature:
    def __init__(self, hp, power, death, inventory=None, attire=None):
        self.base_hp = hp
        self.hp = hp
        self.base_power = power
        
        self.death = death
        self.inventory = inventory
        
        if attire:
            for obj in attire:
                obj.equipment.is_equipped = True
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
                self.drop_item()
                
                print '{} has Died.'.format(self.owner.name)
                self.death(self.owner)
            else:
                print '{} has {} remaining HP.'.format(self.owner.name, self.hp)

    def attack(self, target):
        # assign to self for more attributes.
        # figure out how we will use inscription in doing crit
        # Targeting should effect crit chance and amount
        # Crit-splotion
        crit_effect = 2
        crit_chance = 20
        check_crit = random.randint(0,100)
        damage = self.power
        if check_crit < crit_chance:
            print 'Crit hit'
            damage = (self.power * crit_effect)
            
        if damage > 0:
            attacker = self.owner
            print '{} has hit {} with {} worth of damage!'.format(attacker.name, target.name, damage)
            target.creature.take_damage(damage)
            
    def drop_item(self):
        belongings = []        
        belongings += self.inventory if self.inventory else []        
        belongings += self.attire if self.attire else []

        if belongings:
            most_valued_item = max(belongings, key=lambda x: x.item.value)
            most_valued_item.equipment.is_equipped = False
            most_valued_item.item.drop(self.owner.x, self.owner.y)
        
            print 'Dropped {}.'.format(most_valued_item.name)
        
    def is_slot_empty(self, check_slots):
        items_in_slots = []
        for item_in_bag in self.attire:
            for slot_space in check_slots:
            
                if slot_space in item_in_bag.equipment.equipped_slot:
                    items_in_slots.append(item_in_bag)
                    
        return items_in_slots

        
class Item:
    def __init__(self, weight, value, intensity=0, 
            has_use=None, 
            use_verb=None, 
            inscribe_affect=None
        ):
        self.weight = weight
        self.value = value
        self.intensity = intensity
        self.has_use = has_use
        self.use_verb = use_verb
        self.inscribe_affect = inscribe_affect
    
    def pick_up(self):
        OBJECT_CONTAINER.remove(self.owner)
    
    def drop(self, x, y):
        self.owner.x = x
        self.owner.y = y
        OBJECT_CONTAINER.append(self.owner)
        self.owner.send_to_back()
        
    def use(self, use_on):
        if self.has_use is not None:
            self.has_use(self, use_on.creature, self.use_verb)


inscription_bonus = lambda equipt, attribute: sum(
    script.intensity 
    for script in equipt.inscriptions 
    if script.inscribe_affect == attribute
)

class Equipment:
    def __init__(self, slots, magnitute, optional_slot=True, equipped_slot=None, 
            affect_attribute=None, 
            inscriptions=None,
            can_inscribe=True
        ):
        # Slot Handling
        self.slots = slots
        self.optional_slot = optional_slot
        self.equipped_slot = equipped_slot
        self.is_equipped = False
        
        # Affect Handling
        self.base_magnitute = magnitute
        #self.base_magnitute = magnitute
        self.affect_attribute = affect_attribute
        self.inscriptions = inscriptions
        if inscriptions is None:
            self.inscriptions = []
        self.can_inscribe = can_inscribe

        all_attire = [
            entity.creature.attire 
            for entity in OBJECT_CONTAINER
            if entity.creature
        ]
        if self not in OBJECT_CONTAINER and (self in all_attire):
            self.is_equipped = True
            
    @property
    def magnitute(self):
        if self.inscriptions:
            return self.base_magnitute * (1 + inscription_bonus(self, 'magnitute'))
        return self.base_magnitute
        
        
    def toggle_equip(self, unit):
        if self.is_equipped:
            self.dequip(unit.creature)
        else:
            self.equip(unit.creature)
            
    def equip(self, creature):
        if self.optional_slot:
            user_string = 'Where would you like to equipt?({})'.format(','.join(self.slots))
            select_slot = [raw_input(user_string)]
        else:
            select_slot = self.slots
        
        equipment_in_slot = creature.is_slot_empty(select_slot)
        print select_slot
        if equipment_in_slot:
            for x in equipment_in_slot:
                x.equipment.dequip(creature)
            
        self.is_equipped = True
        self.equipped_slot = select_slot
        creature.inventory.remove(self.owner)
        creature.attire.append(self.owner)
        print 'Now wearing {}.'.format(self.owner.name)
        
    def dequip(self, creature):
        if not self.is_equipped:
            return
        self.is_equipped = False
        self.equipped_slot = None
        creature.attire.remove(self.owner)
        creature.inventory.append(self.owner)
        print 'Taken {} off.'.format(self.owner.name)


def creature_death(corpse):
    corpse.creature = None
    corpse.passable = True
    corpse.name = 'Mangled {} corpse.'.format(corpse.name)
    corpse.representation = '%'
    corpse.send_to_back()        
