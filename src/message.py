
class Message:

    # def moving_message(direction):
        # print 'Player moved {}'.format(direction)


    def attack_message(attacker, target, damge, outcome):
    
        print '{} has hit {} with {} worth of damage!'.format(attacker.owner.name, target.name, damage)
        print '{} has {} remaining HP.'.format(target.name, target.creature.hp)
        