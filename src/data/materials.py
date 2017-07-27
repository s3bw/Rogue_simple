"""      
Each of the materials dictionarys contains a comparitive 'weight', 'rarity' and 'strength' for between material comparisons.
There is also 'strength', 'weight', 'rarirty' and 'value' for the materials within this dictionary.

Material Dictionaries:
- Textile_Data
- Wood_Data
- Metal_Data

"""

Textile_Data = {
    "weight": 4,
    "rarity": 3,
    "strength": 4,
    "textiles": {
        "wool": {
            "special": "warm",
            "strength": 8,
            "weight": 5,
            "value": 6,
            "rarity": 5
        },
        "leather": {
            "strength": 8,
            "weight": 6,
            "value": 8,
            "rarity": 6
        },
        "linen": {
            "strength": 7,
            "weight": 3,
            "value": 5,
            "rarity": 5
        },
        "ramie": {
            "strength": 7,
            "weight": 4,
            "value": 4,
            "rarity": 3
        },
        "hemp": {
            "strength": 6,
            "weight": 4,
            "value": 5,
            "rarity": 3
        },
        "silk": {
            "strength": 6,
            "weight": 2,
            "value": 8,
            "rarity": 7
        },
        "jute": {
            "special": "helpscarrying",
            "strength": 7,
            "weight": 4,
            "value": 6,
            "rarity": 6
        },
        "cotton": {
            "special": "manyresistances",
            "strength": 6,
            "weight": 3,
            "value": 7,
            "rarity": 6
        }
    }
}
    
Wood_Data = {
    "weight": 4,
    "rarity": 3,
    "strength": 4,
    "woods": {
        "fir": {
            "strength": 3,
            "weight": 5,
            "value": 3,
            "rarity": 5
        },
        "spruce": {
            "strength": 6,
            "weight": 6,
            "value": 3,
            "rarity": 3
        },
        "hemlock": {
            "strength": 7,
            "weight": 4,
            "value": 3,
            "rarity": 5
        },
        "redwood": {
            "special": " resistant to everything ",
            "strength": 6,
            "weight": 7,
            "value": 8,
            "rarity": 9
        },
        "hickory": {
            "strength": 6,
            "weight": 8,
            "value": 4,
            "rarity": 4
        },
        "cherry": {
            "strength": 5,
            "weight": 5,
            "value": 7,
            "rarity": 6
        },
        "mahogany": {
            "special": " varying strength",
            "strength": 5,
            "weight": 6,
            "value": 8,
            "rarity": 7
        },
        "oak": {
            "strength": 8,
            "weight": 7,
            "value": 5,
            "rarity": 5
        },
        "pine": {
            "special": " water resistant ",
            "strength": 4,
            "weight": 3,
            "value": 4,
            "rarity": 4
        },
        "teak": {
            "strength": 7,
            "weight": 8,
            "value": 9,
            "rarity": 7
        },
        "cedar": {
            "special": "aromatic",
            "strength": 3,
            "weight": 4,
            "value": 4,
            "rarity": 5
        },
        "birch": {
            "strength": 5,
            "weight": 7,
            "value": 9,
            "rarity": 7
        },
        "beech": {
            "strength": 7,
            "weight": 7,
            "value": 5,
            "rarity": 5
        },
        "rosewood": {
            "special": " dark",
            "strength": 6,
            "weight": 6,
            "value": 8,
            "rarity": 7
        },
        "ash": {
            "strength": 5,
            "weight": 8,
            "value": 4,
            "rarity": 5
        },
        "maple": {
            "special": " shock_resistant",
            "strength": 7,
            "weight": 6,
            "value": 6,
            "rarity": 6
        }
    }
}

Metal_Data = {
    "weight": 5,
    "rarity": 5,
    "strength": 5,
    "metals": {
        "wrought iron": {
            "strength": 4,
            "weight": 7,
            "value": 5,
            "rarity": 3
        },
        "steel": {
            "special": "All resistances",
            "strength": 8,
            "weight": 7,
            "value": 7,
            "rarity": 7
        },
        "iron": {
            "special": "have hp effect",
            "strength": 6,
            "weight": 7,
            "value": 6,
            "rarity": 5
        },
        "alumninium": {
            "special": "long lasting",
            "strength": 3,
            "weight": 3,
            "value": 5,
            "rarity": 4
        },
        "gold": {
            "strength": 3,
            "weight": 7,
            "value": 9,
            "rarity": 8
        },
        "lead": {
            "special": "bonus used as bolt",
            "strength": 4,
            "weight": 9,
            "value": 5,
            "rarity": 5
        },
        "silver": {
            "strength": 4,
            "weight": 5,
            "value": 8,
            "rarity": 7
        },
        "cast iron": {
            "strength": 5,
            "weight": 6,
            "value": 4,
            "rarity": 5
        },
        "tin": {
            "strength": 4,
            "weight": 4,
            "value": 3,
            "rarity": 4
        },
        "pure iron": {
            "strength": 4,
            "weight": 6,
            "value": 3,
            "rarity": 2
        },
        "nickel": {
            "strength": 7,
            "weight": 6,
            "value": 5,
            "rarity": 6
        },
        "white brass": {
            "strength": 4,
            "weight": 6,
            "value": 8,
            "rarity": 7
        },
        "copper": {
            "strength": 5,
            "weight": 5,
            "value": 6,
            "rarity": 6
        },
        "brass": {
            "special": "anti corrosion",
            "strength": 5,
            "weight": 6,
            "value": 7,
            "rarity": 6
        }
    }
}
        