'''      
Each of the materials dictionarys contains a comparitive 'weight', 'rarity' and 'strength' for between material comparisons.
There is also 'strength', 'weight', 'rarirty' and 'value' for the materials within this dictionary.

Material Dictionaries:
- Textile_Data
- Wood_Data
- Metal_Data

'''

Textile_Data = {
    'linen': {
        'strength': 28,
        'value': 5,
        'weight': 12,
        'rarity': 15
    },
    'ramie': {
        'strength': 28,
        'value': 4,
        'weight': 16,
        'rarity': 9
    },
    'leather': {
        'strength': 32,
        'value': 8,
        'weight': 24,
        'rarity': 18
    },
    'wool': {
        'special': 'warm',
        'strength': 32,
        'value': 6,
        'weight': 20,
        'rarity': 15
    },
    'hemp': {
        'strength': 24,
        'value': 5,
        'weight': 16,
        'rarity': 9
    },
    'silk': {
        'strength': 24,
        'value': 8,
        'weight': 8,
        'rarity': 21
    },
    'jute': {
        'special': 'helpscarrying',
        'strength': 28,
        'value': 6,
        'weight': 16,
        'rarity': 18
    },
    'cotton': {
        'special': 'manyresistances',
        'strength': 24,
        'value': 7,
        'weight': 12,
        'rarity': 18
    }
}

    
Wood_Data = {
    'fir': {
        'strength': 12,
        'value': 3,
        'weight': 20,
        'rarity': 15
    },
    'spruce': {
        'strength': 24,
        'value': 3,
        'weight': 24,
        'rarity': 9
    },
    'hemlock': {
        'strength': 28,
        'value': 3,
        'weight': 16,
        'rarity': 15
    },
    'redwood': {
        'special': ' resistant to everything ',
        'strength': 24,
        'value': 8,
        'weight': 28,
        'rarity': 27
    },
    'hickory': {
        'strength': 24,
        'value': 4,
        'weight': 32,
        'rarity': 12
    },
    'cherry': {
        'strength': 20,
        'value': 7,
        'weight': 20,
        'rarity': 18
    },
    'mahogany': {
        'special': ' varying strength',
        'strength': 20,
        'value': 8,
        'weight': 24,
        'rarity': 21
    },
    'oak': {
        'strength': 32,
        'value': 5,
        'weight': 28,
        'rarity': 15
    },
    'pine': {
        'special': ' water resistant ',
        'strength': 16,
        'value': 4,
        'weight': 12,
        'rarity': 12
    },
    'teak': {
        'strength': 28,
        'value': 9,
        'weight': 32,
        'rarity': 21
    },
    'cedar': {
        'special': 'aromatic',
        'strength': 12,
        'value': 4,
        'weight': 16,
        'rarity': 15
    },
    'birch': {
        'strength': 20,
        'value': 9,
        'weight': 28,
        'rarity': 21
    },
    'beech': {
        'strength': 28,
        'value': 5,
        'weight': 28,
        'rarity': 15
    },
    'rosewood': {
        'special': ' dark',
        'strength': 24,
        'value': 8,
        'weight': 24,
        'rarity': 21
    },
    'ash': {
        'strength': 20,
        'value': 4,
        'weight': 32,
        'rarity': 15
    },
    'maple': {
        'special': ' shock_resistant',
        'strength': 28,
        'value': 6,
        'weight': 24,
        'rarity': 18
    }
}


Metal_Data = {
    'steel': {
        'special': 'All resistances',
        'strength': 40,
        'weight': 35,
        'value': 7,
        'rarity': 35
    },
    'copper': {
        'strength': 25,
        'weight': 25,
        'value': 6,
        'rarity': 30
    },
    'nickel': {
        'strength': 35,
        'weight': 30,
        'value': 5,
        'rarity': 30
    },
    'lead': {
        'special': 'bonus used as bolt',
        'strength': 20,
        'weight': 45,
        'value': 5,
        'rarity': 25
    },
    'gold': {
        'strength': 15,
        'weight': 35,
        'value': 9,
        'rarity': 40
    },
    'cast iron': {
        'strength': 25,
        'weight': 30,
        'value': 4,
        'rarity': 25
    },
    'silver': {
        'special': 'burns were beasts',
        'strength': 20,
        'weight': 25,
        'value': 8,
        'rarity': 35
    },
    'tin': {
        'strength': 20,
        'weight': 20,
        'value': 3,
        'rarity': 20
    },
    'iron': {
        'special': 'have hp effect',
        'strength': 30,
        'weight': 35,
        'value': 6,
        'rarity': 25
    },
    'wrought iron': {
        'strength': 20,
        'weight': 35,
        'value': 5,
        'rarity': 15
    },
    'brass': {
        'special': 'anti corrosion',
        'strength': 25,
        'weight': 30,
        'value': 7,
        'rarity': 30
    },
    'white brass': {
        'special': 'Crits'
        'strength': 18,
        'weight': 30,
        'value': 8,
        'rarity': 35
    },
    'alumninium': {
        'special': 'long lasting',
        'strength': 15,
        'weight': 15,
        'value': 5,
        'rarity': 20
    },
    'pure iron': {
        'strength': 20,
        'weight': 30,
        'value': 3,
        'rarity': 10
    }
}
