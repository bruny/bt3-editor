# Item FAQ http://www.bardstaleonline.com/files/!docs/bt3-faq-by-yuandy.txt

# Ref http://bardstaleonline.com/files/!docs/bt1-3-items.txt
# dos2unix bt1-3-items.txt
# cat bt1-3-items.txt | cut -c 40- | awk -IFS="\t" '{printf("\"%s\", ", $0)}'
# Not quite correct
items = ['-EMPTY SLOT-', 'Torch', 'Lamp', 'Broadsword', 'Short Sword', 'Dagger', 'War Axe', 'Halbard', 'Long Bow', 'Staff',
         'Buckler', 'Tower Shield', 'Leather Armor', 'Chain Mail', 'Scale Armor', 'Plate Armor', 'Robes', 'Helm',
         'Leather Gloves', 'Gauntlets', 'Mandolin', 'Spear', 'Arrows', 'Mthr Sword', 'Mthr Shield', 'Mthr Chain',
         'Mthr Scale', 'Giant Fgn', 'Mthr Bracers', 'Bardsword', 'Fire Horn', 'Litewand', 'Mthr Dagger', 'Mthr Helm',
         'Mthr Gloves', 'Mthr Axe', 'Shuriken', 'Mthr Plate', 'Molten Fgn', 'Spell Spear', 'Shield Ring',
         'Fin\'s Flute', 'Kael\'s Axe', 'Mthr Arrows', 'Dayblade', 'Shield Staff', 'Elf Cloak', 'Hawkblade',
         'Admt Sword', 'Admt Shield', 'Admt Helm', 'Admt Gloves', 'Pureblade', 'Boomerang', 'Ali\'s Carpet',
         'Luckshield', 'Dozer Fgn', 'Admt Chain', 'Death Stars', 'Admt Plate', 'Admt Bracers', 'Slayer Fgn',
         'Pure Shield', 'Mage Staff', 'War Staff', 'Thief Dagger', 'Soul Mace', 'Ogrewand', 'Kato\'s bracer',
         'Sorcerstaff', 'Galt\'s Flute', 'Frost Horn', 'Ag\'s Arrows', 'Dmnd Shield', 'Bard Bow', 'Dmnd Helm',
         'Elf Boots', 'Vanquisher Fgn', 'Conjurstaff', 'Staff of Lor', 'Flame Sword', 'Powerstaff', 'Breath Ring',
         'Dragonshield', 'Dmnd Plate', 'Wargloves', 'Wizhelm', 'Dragonwand', 'Deathring', 'Crystal Sword',
         'Speedboots', 'Flame Horn', 'Zen Arrows', 'Deathdrum', 'Pipes of Pan', 'Power Ring', 'Song Axe',
         'Trick Brick', 'Dragon Fgn', 'Mage Fgn', 'Troll Ring', 'Aram\'s Knife', 'Angra\'s Eye', 'Herb Fgn',
         'Master Wand', 'Brothers Fgn', 'Dynamite', 'Thor\'s Hammer', 'Stoneblade', 'Holy Handgrenade', 'Masterkey',
         'Nospin Ring', 'Crystal Lens', 'Smokey Lens', 'Black Lens', 'Sphere of Lanatir', 'Wand of Power', 'Acorn',
         'Wineskin', 'Nightspear', 'Tslotha\'s Head', 'Tslotha\'s Heart', 'Arefolia', 'Valarian\'s Bow',
         'Arws of Life', 'Canteen', 'Titan Plate', 'Titan Shield', 'Titan Helm', 'Fire Spear', 'Willow Flute',
         'Firebrand', 'Holy Sword', 'Wand of Fury', 'Lightstar', 'Crown of Truth', 'Belt of Alliria', 'Crystal Key',
         'Tao Ring', 'Stealth Arrows', 'Yellow Staff', 'Steady Eye', 'Divine Halbard', 'Incense', 'I-ching',
         'White Rose', 'Blue Rose', 'Red Rose', 'Yellow Rose', 'Rainbow Rose', 'Magic Triangle', 'Hammer of Wrath',
         'Ferofist\'s Helm', 'Helm of Justice', 'Sceadu\'s Cloak', 'Shadelance', 'Black Arrows', 'Werra\'s Shield',
         'Strifespear', 'Sheetmusic', 'Right Key', 'Left Key', 'Lever', 'Nut', 'Bolt', 'Spanner', 'Shadow Lock',
         'Shadow Door', 'Misericorde', 'Holy Avenger', 'Red\'s Stiletto', 'Kali\'s Garrote', 'Flame Knife',
         'Shadowshiv', 'Heartseeker', 'Dmnd Scale', 'Holy TNT', 'Eternal Torch', 'Oscon\'s Staff',
         'Angel\'s Ring', 'Deathhorn', 'Staff of Mangar', 'Tesla Ring', 'Dmnd Bracers', 'Death Fgn', 'Thunder Sword',
         'Poison Dagger', 'Spark Blade', 'Galvanic Oboe', 'Blood Mesh Robe', 'Tung Shield', 'Tung Plate',
         'Minstrels Glove', 'Hunters Cloak', 'Death Hammer', 'Harmonic Gem', 'Soothing Balm', 'Mages Cloak',
         'Familiar Fgn', 'Hourglass', 'Thieves Hood', 'Surehand Amulet', 'Thieves Dart', 'Shrill Flute',
         'Angel\'s Harp', 'The Book', 'Troth Lance', 'Dmnd Suit', 'Dmnd Flail', 'Purple Heart', 'Titan Bracers',
         'Eelskin Tunic', 'Sorcerer\'s Hood', 'Dmnd Staff', 'Crystal Gem', 'Wand of Force', 'Cli Lyre', 'Gods\' Blade',
         'Mthr Suit', 'Titan Suit', 'Mages Glove', 'Flare Crystal', 'Holy Missile', 'Youth Potion', 'Hunter Blade',
         'Staff of Gods', 'Horn of Gods', 'Water', 'Spirits', 'Water of Life', 'Dragon Blood', 'Molten Tar']


class item(object):
    _id = 0
    _equipped = False   # 0 or 1; if 81, then it is "not known", 02 - can't use
    _charges = 0

    # FIXME TODO Indicator whether usable by a particular class
    # FIXME TODO Comments describing each item above

    def __init__(self, id=None, equipped=None, charges=None):
        self._id = id
        self._equipped = equipped
        self._charges = charges
        # print self._id

    @property
    def name(self):
        return items[self._id]

    def as_formatted_string(self):
        return '{} - {} - {}'.format (self.name, self._charges, self._equipped)