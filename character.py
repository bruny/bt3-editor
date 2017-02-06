
from binascii import hexlify

classes = ['Warrior', 'Wizard', 'Sorcerer', 'Conjurer', 'Magician', 'Rogue', 'Bard', 'Paladin', 'Hunter', 'Monk',
           'Archmage', 'Chronomancer', 'Geomancer', 'Monster'] # fill to 255 with monster slots
races = ['Human', 'Elf', '', 'Hobbit', '', 'Half-Orc', 'Gnome']
sexes = ['Male', 'Female']
status = ['OK', '', 'Old', '', 'Dead', '', 'Poisoned']  # Stoned, Paralyzed, Possessed, Nuts

class character(object):
    _bindata= None

    def __init__(self):
        pass

    def from_bindata(self, bindata):
        self._bindata = bindata

    @property
    def bindata(self):
        # Print the bin data as hex
        s = t = ''
        for el in self._bindata:
            s += hexlify(el) + ' '
            t += str(int(hexlify(el),16)) + '\t' # Numeric representation
        return '{0:20}\t{1:<10}'.format("char name", s)

    @property
    def char_name(self):
        charname = ''
        bin = self._bindata[0:16]
        for c in bin[1:]:
            a = hexlify(c)
            charname += chr(int(hex(int(a,16)-0x80), 16))
        return charname

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
        return classes[int(hexlify(bin),16)]

    @property
    def char_race(self):
        bin = self._bindata[43]
        return races[int(hexlify(bin),16)]

    @property
    def char_sex(self):
        bin = self._bindata[44]
        return sexes[int(hexlify(bin),16)]