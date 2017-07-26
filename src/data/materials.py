# Metals and Woods
# http://www.technologystudent.com/designpro/matintro1.htm

# Textiles
# http://www.textileschool.com/articles/330/type-of-fabrics

# Fibers
# https://en.wikipedia.org/wiki/Ramie

# values = {

# 'wood' 
    # 'natural'
        # #hard
        # 'oak' - heavy strong common, med value
        # 'maple' - hard shock resistant less common, above med
        # 'mahogany' - high value, above med weight, strength varies
        # 'cherry' - ave strong, above med value 
        # 'rosewood' - hard, dark, high value above med weight
        # 'teak' - extremly heavy, strong, above high value
        # 'ash' - heavy, below average value
        # # soft
        # 'pine' - soft, light weight, water resistant 
        # 'hickory' - thick and very heavy  - structural purposes
        # 'beech' - hard strong heavy
        # 'birch' - rare and expensive, heavy 
        # 'cedar' - aromatic, light, brittle
        # 'redwood' - extremely rare, resistant to sun moisture and insects
        # 'hemlock' - light wieght, strong, common 
        # 'fir' - soft, common 
        # 'spruce' - strong hard, very common.

# 'textiles'
    # 'natural'
        # 'cotton' - soft all-season - high value, light wieght 
        # 'silk' - very high value soft,low weight 
        # 'linen' - durable, common - med value, light weight 
        # 'wool' - very strong, soft, warm, above medium value , above med wieght 
        # 'leather' - firm - very high value - weighter than others heavy 
        # 'ramie' - very common very light - medium strength, med wight 
        # 'hemp' -long lasting, very common , med value med wight 
        # 'jute' - strong, (packaging) uncommon, med weight 
        
# 'metal'
    # 'ferrous' less rare - for the bottom metals
        # 'pure iron' - low value
        # 'iron' - hardy - effect hp - above average value
        # 'alumninium' - soft, very light, - long lasting
        # 'cast iron' - corrodes - hard skin
        # 'steel' - resistant and hard
        # 'wrought iron' - use in barricading brittle
        
    # 'non-ferrous' more rare
        # 'copper' - beaten into shape - medium weight - rusts
        # 'brass' - resistant to corrosion - cracks - made into instruments
        # 'white brass' - very brittle - high value 
        # 'silver' - soft, not as soft as gold - high value
        # 'lead' - very heavy - soft - medium value - usage in bolts
        # 'tin' - last a little longer, but soft - low value
        # 'gold' - very soft - high value
        # 'nickel' - med value, tougher than iron

# value, weight, rarity, stregth, special_attribute
# higher value, more weight, high rarity, hard strength

# I fell like the material globals should have less effect on the extremes (rarity)
# I should do a random material comparisons to balance them after. e.g. jute vs beech (etc.)

# 'wood': weight=4, rarity=3, stregth=4
'oak', 5, 7, 5, 8
'maple',6, 6, 6, 7, "shock_resistant"
'mahogany',  8, 6, 7, 5, "varying strength"
'cherry',7, 5, 6, 5
'rosewood',8, 6, 7, 6, "dark"
'teak',9, 8, 7, 7
'ash',4, 8, 5, 5
'pine',4, 3, 4, 4, "water resistant" 
'hickory',4, 8, 4, 6
'beech',5, 7, 5, 7
'birch',9, 7, 7, 5
'cedar',4, 4, 5, 3, "aromatic"
'redwood',8, 7, 9, 6, "resistant to everything" 
'hemlock',3, 4, 5, 7
'fir',3, 5, 5, 3
'spruce',3, 6, 3, 6

# 'textiles', weight=2, rarity=4, stregth=3
# allows for macro level balacing

    # 'cotton',7, 3, 6, 6, "many resistances" 
    # 'silk',8, 2, 7, 6
    # 'linen',5, 3, 5, 7
    # 'wool',6, 5, 5, 8, "warm"
    # 'leather',8, 6, 6, 8
    # 'ramie',4, 4, 3, 7
    # 'hemp',5, 4, 3, 6
    # 'jute',6, 4, 6, 7, "helps carrying"

{
  "fir": {
    "special": nan,
    "strength": 3L,
    "weight": 5L,
    "value": 3L,
    "rarity": 5L
  },
  "spruce": {
    "special": nan,
    "strength": 6L,
    "weight": 6L,
    "value": 3L,
    "rarity": 3L
  },
  "hemlock": {
    "special": nan,
    "strength": 7L,
    "weight": 4L,
    "value": 3L,
    "rarity": 5L
  },
  "redwood": {
    "special": " resistant to everything ",
    "strength": 6L,
    "weight": 7L,
    "value": 8L,
    "rarity": 9L
  },
  "hickory": {
    "special": nan,
    "strength": 6L,
    "weight": 8L,
    "value": 4L,
    "rarity": 4L
  },
  "cherry": {
    "special": nan,
    "strength": 5L,
    "weight": 5L,
    "value": 7L,
    "rarity": 6L
  },
  "mahogany": {
    "special": " varying strength",
    "strength": 5L,
    "weight": 6L,
    "value": 8L,
    "rarity": 7L
  },
  "oak": {
    "special": nan,
    "strength": 8L,
    "weight": 7L,
    "value": 5L,
    "rarity": 5L
  },
  "pine": {
    "special": " water resistant ",
    "strength": 4L,
    "weight": 3L,
    "value": 4L,
    "rarity": 4L
  },
  "teak": {
    "special": nan,
    "strength": 7L,
    "weight": 8L,
    "value": 9L,
    "rarity": 7L
  },
  "cedar": {
    "special": " aromatic",
    "strength": 3L,
    "weight": 4L,
    "value": 4L,
    "rarity": 5L
  },
  "birch": {
    "special": nan,
    "strength": 5L,
    "weight": 7L,
    "value": 9L,
    "rarity": 7L
  },
  "beech": {
    "special": nan,
    "strength": 7L,
    "weight": 7L,
    "value": 5L,
    "rarity": 5L
  },
  "rosewood": {
    "special": " dark",
    "strength": 6L,
    "weight": 6L,
    "value": 8L,
    "rarity": 7L
  },
  "ash": {
    "special": nan,
    "strength": 5L,
    "weight": 8L,
    "value": 4L,
    "rarity": 5L
  },
  "maple": {
    "special": " shock_resistant",
    "strength": 7L,
    "weight": 6L,
    "value": 6L,
    "rarity": 6L
  }
}

Metal_Data = {
    "metal": {
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
}
        