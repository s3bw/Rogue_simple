
```
 https://gamedev.stackexchange.com/questions/85871/how-should-loot-be-distributed-across-dungeon-levels
 if head & Metal = Helmet
 if head & Wool = Cap
  Then mention material + item:
   Gold Helmet/ Steel Helmet

 Primary Materials have defence/offense attribute:
 e.g.   50, if gold 50 * 0.2
 
            if steel 50 * 0.9

 representation based on class
    --> e.g. tier 1: ^
    --> e.g. tier 2: n
    --> e.g. tier 3: M
```
# Metals

Metal
## Ferrous
Less rare - for the bottom metals
- **pure iron** - low value
- **iron** - hardy - effect hp - above average value
- **alumninium** - soft, very light, - long lasting
- **cast iron** - corrodes - hard skin
- **steel** - resistant and hard
- **wrought iron** - use in barricading brittle

## Non-ferrous
More rare
- **copper** - beaten into shape - medium weight - rusts
- **brass** - resistant to corrosion - cracks - made into instruments
- **white brass** - very brittle - high value 
- **silver** - soft, not as soft as gold - high value
- **lead** - very heavy - soft - medium value - usage in bolts
- **tin** - last a little longer, but soft - low value
- **gold** - very soft - high value
- **nickel** - med value, tougher than iron


http://www.technologystudent.com/designpro/matintro1.htm

---

# Woods

Woods - natural

## Hard

- **oak** - heavy strong common, med value
- **maple** - hard shock resistant less common, above med
- **mahogany** - high value, above med weight, strength varies
- **cherry** - ave strong, above med value 
- **rosewood** - hard, dark, high value above med weight
- **teak** - extremly heavy, strong, above high value
- **ash** - heavy, below average value

## Soft

- **pine** - soft, light weight, water resistant 
- **hickory** - thick and very heavy  - structural purposes
- **beech** - hard strong heavy
- **birch** - rare and expensive, heavy 
- **cedar** - aromatic, light, brittle
- **redwood** - extremely rare, resistant to sun moisture and insects
- **hemlock** - light wieght, strong, common 
- **fir** - soft, common 
- **spruce** - strong hard, very common.

---

# Textiles

Natural

- **cotton** - soft all-season - high value, light wieght 
- **silk** - very high value soft,low weight 
- **linen** - durable, common - med value, light weight 
- **wool** - very strong, soft, warm, above medium value , above med wieght 
- **leather** - firm - very high value - weighter than others heavy 
- **ramie** - very common very light - medium strength, med wight 
- **hemp** -long lasting, very common , med value med wight 
- **jute** - strong, (packaging) uncommon, med weight 

http://www.textileschool.com/articles/330/type-of-fabrics

---

# Fibers

For more fibers look into [animal thread](https://en.wikipedia.org/wiki/Ramie)

# Notes:

value, weight, rarity, stregth, special_attribute
higher value, more weight, high rarity, hard strength

I can add animal textiles 
I fell like the material globals should have less effect on the extremes (rarity)
I should do a random material comparisons to balance them after. e.g. jute vs beech (etc.)

For Consistant Ratings:

No mention of attribute `== Average. 5` 
Mention of edge case `== 3 or 7` (e.g. light, heavy)
Mention of very case `== 2 or 8` (e.g. very light, very heavy)
Mention of extreme edge case `== 1 or 9` (e.g extremely heavy)
Mention of soft case `== 4 or 6` (no very heavy)
