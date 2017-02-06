
from binascii import hexlify
from items import item

classes = ['Warrior', 'Wizard', 'Sorcerer', 'Conjurer', 'Magician', 'Rogue', 'Bard', 'Paladin', 'Hunter', 'Monk',
           'Archmage', 'Chronomancer', 'Geomancer', 'Monster'] # fill to 255 with monster slots
races = ['Human', 'Elf', '', 'Hobbit', '', 'Half-Orc', 'Gnome']
sexes = ['Male', 'Female']
status = ['OK', '', 'Old', '', 'Dead', '', 'Poisoned']  # Stoned, Paralyzed, Possessed, Nuts


class Character(object):
    _bindata = None

    def __init__(self):
        pass

    def from_bindata(self, bindata):
        self._bindata = bindata

    def __data_as_hexstring(self, data):
        s = t = ''
        for el in data:
            s += hexlify(el) + ' '
            t += str(int(hexlify(el), 16)) + '\t'   # Numeric representation
        return s

    @property
    def isparty(self):
        return self.char_name.startswith('*')

    @property
    def bindata(self):
        # Print the bin data as hex
        """
        s = t = ''
        for el in self._bindata:
            s += hexlify(el) + ' '
            t += str(int(hexlify(el),16)) + '\t' # Numeric representation
        """
        s = self.__data_as_hexstring(self._bindata)
        return '{0:20}\t{1:<10}'.format("char name", s)

    @property
    def char_name(self):
        # If charname starts with *, it's a party; need to work out how parties are structured
        charname = ''
        bin = self._bindata[0:16]
        for c in bin[1:]:
            a = hexlify(c)
            charname += chr(int(hex(int(a, 16)-0x80), 16))
        return charname

    @property
    def char_hexname(self):
        bin = self._bindata[0:16]
        return hexlify(bin)

    @property
    def char_attrs(self):
        bin = self._bindata[17:22]
        binattrs = hexlify(bin)
        listattrs = map(ord, binattrs.decode('hex'))
        return listattrs

    @property
    def char_exp(self):
        bin = self._bindata[22:26]
        print hexlify(bin)
        return int(hexlify(bin[::-1]), 16)
        pass

    @property
    def char_gold(self):
        bin = self._bindata[26:30]
        print hexlify(bin)
        return int(hexlify(bin[::-1]), 16)
        pass

    @property
    def char_lvl_curr(self):
        bin = self._bindata[30:32]
        return int(hexlify(bin[::-1]), 16)
        pass

    @property
    def char_lvl_max(self):
        bin = self._bindata[32:34]
        return int(hexlify(bin[::-1]), 16)
        pass

    @property
    def char_hp_curr(self):
        bin = self._bindata[34:36]
        return int(hexlify(bin[::-1]), 16)
        pass

    @property
    def char_hp_max(self):
        bin = self._bindata[36:38]
        return int(hexlify(bin[::-1]), 16)
        pass

    @property
    def char_sp_curr(self):
        bin = self._bindata[38:40]
        return int(hexlify(bin[::-1]), 16)
        pass

    @property
    def char_sp_max(self):
        bin = self._bindata[40:42]
        return int(hexlify(bin[::-1]), 16)
        pass

    @property
    def char_class(self):
        bin = self._bindata[42]
        return classes[int(hexlify(bin), 16)]

    @property
    def char_race(self):
        bin = self._bindata[43]
        return races[int(hexlify(bin), 16)]

    @property
    def char_sex(self):
        bin = self._bindata[44]
        return sexes[int(hexlify(bin), 16)]

    @property
    def char_portrait(self):
        bin = self._bindata[45]
        return int(hexlify(bin), 16)

    @property
    def char_status(self):
        bin = self._bindata[46]
        return status[int(hexlify(bin), 16)]

    @property
    def char_ac(self):
        bin = self._bindata[47]
        return 10 - int(hexlify(bin), 16)

    # offset 48 unidentified

    # Items: 12 slots of 3 bytes (49 + 36 = 85)
    @property
    def char_items(self):
        items = []
        for i in range(0,12):
            bin = self._bindata[48+(i*3)+1:48+(i*3)+3+1]
            ite = item(id=int(hexlify(bin[1]), 16), equipped=hexlify(bin[0]), charges=hexlify(bin[2]))
            items.append(ite.as_formatted_string())
            #print ite
        return items

    # Unidentified 16 bytes (85 + 16 = 101)

    # Special abilities: 3 bytes
    # These are percentages, refer to http://stackoverflow.com/questions/15852122/hex-transparency-in-colors,
    # specifically http://stackoverflow.com/a/27435811 and http://stackoverflow.com/a/29141832
    @property
    def char_abilities(self):
        """
        Bard: ability 0 is number of bard tunes left
        Thief: ability 0 = disarm traps, 1 = identify chest, identify item, 2 = hide in shadows, critical hit
        Hunter: ability 0 = critical hit
        """
        abilities = []
        for i in range(0, 3):
            bin = self._bindata[101 + i]
            x = int(hexlify(bin), 16)
            d = int(float(x) / 255 * 100)
            abilities.append(d)
        return abilities

    # Unidentified 24 bytes (104 + 24 = 128), first char bytes are possibly spell data?

    @property
    def unidentifieddata(self):
        # This data is unknown at this time
        # ? Number of attacks? Mission flags?
        return '{0} / {1} / {2}'.format(self.__data_as_hexstring(self._bindata[48]),
                                        self.__data_as_hexstring(self._bindata[85:101]),
                                        self.__data_as_hexstring(self._bindata[104:128]))
