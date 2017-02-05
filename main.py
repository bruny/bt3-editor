#!/usr/bin/python
# -*- coding: UTF-8 -*-

# http://www.virtualapple.org/docs/bards.tale.3.ed.txt
# https://groups.google.com/forum/#!topic/comp.sys.apple2/2a59aY9JvNM - reading the name
# https://www.gamefaqs.com/pc/564572-the-bards-tale-3-the-thief-of-fate/faqs/50117 - C64 hex
# http://www.gamefaqs.com/pc/564572-the-bards-tale-3-the-thief-of-fate/faqs/27932 - item FAQ

# Note - party events (including current characters) must be stored separately since hitting events doesn't update
# characters

# Adding items - e.g. Valarian's Bow/Arros of Life is sufficient to pass a lot of checks - as long as one party member has it
# Possibly, we can't just change our location unless some other check has been matched
# e.g. Valarian's Twr level 4 requires noting that the acorns have been placed and watered to allow access

import argparse
import mmap
from binascii import hexlify
import codecs
import sys
#import locale
from items import item

def reversehex3(hexes):
    # Note that we expect a list of integers in base 10 format
    print hexes
    hexes.reverse()
    print hexes

# Item FAQ http://www.bardstaleonline.com/files/!docs/bt3-faq-by-yuandy.txt

def reversehex2(hexes):
    # Note that we expect a list of binary values e.g. \x89 etc
    print hexes

    hexes.reverse()
    print hexes
    joined = ''.join(map(str, hexes))
    print joined    # Str at this stage
    print type(joined)

    print hexlify(joined)
    print int(hexlify(joined), 16)   # Here we are
    return int(hexlify(joined), 16)

# Given a binary hex value (e.g. c1), returns the numeric value (93)
def bin2num(bin):
    return map(ord, hexlify(bin).decode('hex'))

# Given a binary value (i.e. directly read), returns the hex value
def bin2hex(bin):
    return hexlify(bin)

def reversehex(hexes):
    print hexes

    hexes.reverse()
    print hexes
    joined = ''.join(map(str, hexes))
    print joined    # Str at this stage
    print type(joined)
    hexval = hex(int(joined,16))
    print int(hexval, 16)   # Here we are
    return int(hexval, 16)

classes = ['Warrior', 'Wizard', 'Sorcerer', 'Conjurer', 'Magician', 'Rogue', 'Bard', 'Paladin', 'Hunter', 'Monk',
           'Archmage', 'Chronomancer', 'Geomancer', 'Monster'] # fill to 255 with monster slots
races = ['Human', 'Elf', '', 'Hobbit', '', 'Half-Orc', 'Gnome']
sexes = ['Male', 'Female']
status = ['OK', '', 'Old', '', 'Dead', '', 'Poisoned']  # Stoned, Paralyzed, Possessed, Nuts
direction = ['North', 'South', 'East', 'West']

dimensions = ['', 'Earth', 'Arboria', 'Gelidia']


class bt3char(object):
    def __init__(self):
        pass

def get_name(rawdata):
    charname = ''
    for c in rawdata[1:]:
        a = hexlify(c)
        charname += chr(int(hex(int(a,16)-0x80), 16))

    return charname

# Skara Brae =

def next_character(char_start_pos, current_pos):
    CHAR_LENGTH = 128

    skip = CHAR_LENGTH - (current_pos - char_start_pos)

    print 'Current pos is {0}, need to skip {1} bytes'.format(current_pos, skip)

    return skip

def increase_xp(char_start_pos):
    # FIXME TODO
    mm.seek(char_start_pos)


def read_chars(mm):
    # Set the start so we can ffwd to the next char if an exception occurs
    start = mm.tell()

    print 'Starting pos = ' + str(start)
    name = mm.read(17)
    print name
    binname = hexlify(name)
    print binname

    try:
        charname = get_name(name)


        # If charname starts with *, it's a party; need to work out how parties are structured

        # We should be at position 141582 + FF, reading through to 141587
        attrs = mm.read(5)
        binattrs = hexlify(attrs)
        listattrs = map(ord, binattrs.decode('hex'))

        # Now read the next 4 digits
        exp = mm.read(4)[::-1]
        gold = mm.read(4)[::-1]

        lvl_curr = mm.read(2)[::-1]
        lvl_old = mm.read(2)[::-1]

        hp_curr = mm.read(2)[::-1]
        hp_max = mm.read(2)[::-1]

        sp_curr = mm.read(2)[::-1]
        sp_max = mm.read(2)[::-1]

        char_class = mm.read(1)
        char_race = mm.read(1)
        char_sex = mm.read(1)

        char_picture = mm.read(1)
        char_status = mm.read(1)
        ac = mm.read(1)

        data2 = mm.read(1)

        # 23 for Farren is 35 - bards songs

        # 11 / 09 / 10
        # 1d / 18 / 1c
        # 29 / 24 / 28

        # Slyter and Berond have hunter ability at this pos?
        #               kipped data is 00 / 000000000000000000000000000000001d181c000000000000000000000000000000000000000000000000
        # Char1
        # Disarm = 1 (0), Identify = 3 (10), Hide/Critical = 7% (20)
        #         Skipped data is      00 / 00000000000000000000000000000000000a14000000000000000000000000000000000000000000000000
        # Character with Disarm Traps = 50, Identify Chest = 50:
        #         Skipped data is 36 / 00 / 00000000000000000000000000000000323200000000000000000000000000000000000000000000000000
        # Farren  Skipped data is 21 / 00 / 0000000000000000000000000000000023fc00000000160a0e0c0900000080030000000000000000000000
        # Ferodo  Skipped data is 21 / 00 / 00000000000000000000000000000000edf7d90000000c0f120e0c00000080030000000000000000000000
        # Agnon   Skipped data is 36 / 00 / 00000000000000000001c000000000000000000000000f140c0c0b00000080030000000000000000000000
        # Slyther Skipped data is 21 / 00 / 00000000000000000000000000000000d70000000000130910140b00000080030000000000000000000000
        # Berond  Skipped data is 21 / 00 / 00000000000000000000000000000000cf0000000000000000000000000080030000000000000000000000
        # Taeris  Skipped data is 37 / 00 / fffffffffffffffffffe000000000000000000000000000000000000000080030000000000000000000000
        # Markus  Skipped data is 36 / 00 / fffffffffffffffffffe000000000000000000000000000000000000000080030000000000000000000000
        # After learning Gilles Gills
        # Markus  Skipped data is 36 / 00 / fffffffffffffffffffe000000000020000000000000000000000000000080030000000000000000000000



        # Items
        for i in range(0,12):
            # FIXME TODO Wrapping is wrong here
            equipped = mm.read(1)   # 0 or 1; if 81, then it is "not known", 02 - can't use
            id = mm.read(1)
            charges = mm.read(1)
            ite = item(id=int(bin2hex(id), 16), equipped=bin2hex(equipped), charges=bin2hex(charges))

            print ite.as_formatted_string()

        # We have read 85 bytes, each char is 128
        data3 = mm.read(16)
        # These are percentages - refer to http://online.sfsu.edu/chrism/hexval.html
        # http://stackoverflow.com/questions/15852122/hex-transparency-in-colors
        # http://stackoverflow.com/a/27435811
        specials1 = mm.read(1)
        specials2 = mm.read(1)
        specials3 = mm.read(1)
        data4 = mm.read(24)
        # first 20 characters likely to be spells? 01 for agnon - all zeroes except chrono

        print 'Name is {0} (binary = {1}, hex = {2}'.format(charname, name, binname)
        print '\tAttributes = {0} (binary = {1})'.format(listattrs, binattrs)
        print '\tStatus is {0}'.format(status[int(hexlify(char_status),16)])
        print '\tCharacter is a {0} {1} {2}'.format(sexes[int(hexlify(char_sex),16)],
                                                  races[int(hexlify(char_race),16)],
                                                  classes[int(hexlify(char_class),16)])
        print '\tExp = {}, Gold = {}, AC = {}'.format(int(hexlify(exp), 16),
                                                    int(hexlify(gold), 16),
                                                    10 - int(hexlify(ac),16))
        print '\tLvl is {}/{}, HP is {}/{}, SP is {}/{}'.format(int(hexlify(lvl_curr), 16),
                                                              int(hexlify(lvl_old), 16),
                                                              int(hexlify(hp_curr), 16),
                                                              int(hexlify(hp_max), 16),
                                                              int(hexlify(sp_curr), 16),
                                                              int(hexlify(sp_max), 16))
        print '\tSpecial abilities are {0}, {1}, {2}'.format(int(hexlify(specials1), 16),
                                                           int(hexlify(specials2), 16),
                                                           int(hexlify(specials3), 16))

        print '\tSkipped data is {} / {} / {}'.format(hexlify(data2), hexlify(data3), hexlify(data4))
        print 'SPOT IS NOW ' + str(mm.tell())
        print


        #mm.read(128-80)
        #mm.read(2480)
    except Exception as e:
        print e.message
        #print 'WARN Unable to get name, possible no char here'
        charname = 'FIXME'
        mm.seek(start + 128)

# Skara Brae appears pos 47582 - 47591 on boot disk, can't find Wilderness or Catacombs
#

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Parse BT3 char disk')
    parser.add_argument('--start', type=int, default=0)
    parser.add_argument('--length', type=int, default=0)
    args = parser.parse_args()

    #disk = "chardisk.d64"
    disk = "14-valarian4.d64"

    if args.start > 0:
        print "Reading {0} bytes from pos {1}".format(args.length, args.start)
        #for disk in ['chardisk.d64', 'chardisk before arboria.d64', 'chardisk skara brae.d64', 'chardisk tarjan 1.d64', 'chardisk wilderness.d64']:
        #for disk in ['01-wilderness.d64', '02-skarabrae.d64', '03-catacombs1.d64', '04-catacombs2.d64', '05-tunnels1.d64', '06-tunnels2.d64',
        #             '07-tunnels3.d64', '08-tunnels4.d64', '09-arboria.d64', '10-caeria.d64',
        #             '10-lakepalace1.d64', '11-pit1.d64', '11-valarian1.d64', '12-valarian2.d64', '13-valarian3.d64', '15-gelidia.d64',
        #             '16-keep1.d64', '17-keep2.d64']:
        for disk in ['13-valarian3.d64', '13-valarian3-acorn.d64']:
            with open(disk, 'r+b') as di:
                mm = mmap.mmap(di.fileno(), 0)
                mm.seek(args.start)
                data = mm.read(args.length)
                s = t = ''
                for el in data:
                    s += hexlify(el) + ' '
                    t += str(int(hexlify(el),16)) + '\t' # Numeric representation
                print '\t{0:25}\t\t\t\t{1:<10}'.format(disk, s)
                #print '\t{0:25}\t\t\t\t{1:<10}'.format(disk, t)


        sys.exit(0)

    """ Show how to convert a readable name to the hex string to find
    """
    if 1:
        name = 'aaaa'
        hexname = []
        offset = hexlify(name)
        print offset
        for i in name:
            hexname.append(hex(ord(i)+0x80))
            #print hex(ord(i))   # Readable string
            #print hex(ord(i)+0x80)  # Written string on disk
        print ' '.join(hexname)


    #reversehex([b'ba', b'a4', b'02', b'00'])
    #sys.exit(-1)
    # Camp - 146687 (1-34)
    start = 139775
    start_save_roster = 139775
    start_camp_roster = 144127
    #start = 144895

    # Current save - 139775
    # Saved game character roster starts at 139775, for 27 x 128 byte records
    # Roster starts at 144127 (i.e. characters in camp) for 34 x 128 byte records

    #... 3074 bytes later
    # 145921 = Start of *Interplayers (started with AA) (16 chars)
    # ... 2048 bytes later
    # 147969 = Start of *Heroes
    # 148096 = Start of Storage1
    # 146176 = Start of Gems1
    # 145936 = Start of Ironpants (first instance)
    # 146688 = Start of Ironpants (second instance)



    with open(disk, 'r+b') as di:

        #09 through 18 (09, 0A, 0B, 0C, 0D, 0E, 0F, 10, 11, 12)

        mm = mmap.mmap(di.fileno(), 0)
        # 141952/53
        # 143619 - NO dungeon? 1f = arboria, 20 = ciera brannia?
        #  - might be offset (1d = wilderness, 1e - skara brae
        # 143620 - NO dimension? (05 = arboria?)
        # 143621 - NO dungeon? 00 - wilderness, 02 - skara brae, 04 - dungeon 1
        # 143628 - NI dungeon? 00 - wilderness, 01 - skara brae
        #  or 143728? NO 0A = palace, 0F = ciara brannia?

        # No difference when saving time-of-day (between e.g. noon and afternoon)
        # 143720 for dungeon? 01 - skara brae, 02 - wilderness, NO

        # 140822?
        # Compared between 143104 to 143892
        # Cearia Brannia
        #E6 2D 84 12 4C 7F 14 C5 EF 98 AE 3E 04 D3 F1 B4 6F 8C F0 30 8B 61 04 19 13 5E 28 1B E0 61 15 C7 C4 C9 9A 36 79 C5 1E B1 3C CF 21 59 DF E4 F9 F2 65 EB 01 47 AC 40 66 36 8B 77 BB 8A 29 F4 21 15 EE 75 1B 46 FD BC 1A 11 6E E6 2B D9 F9 51 1B 46 FD BC 1A 11 6E EC E2 8A 7D 08 45 7B 3F AA A3 68 DC 2D C6 62 C1 6B 26 8D 11 4E F8 68 45 42 C3 E5 54 6C 6C 9A 9B A6 54 F2 03 53 CC 9B A6 4D D3 26 E9 97 34 CA 9E 64 DD 35 37 4E 8D D3 2E 69 02 39 A6 29 1B 46 FD 04 23 71 17 51 B8 93 88 B0 9B D7 06 7F 38 22 82 5F CE FF 53 F1 4F 9C 2F C1 D1 51 27 11 51 35 EF 15 14 A0 90 30 0A EB 50 0A 11 4C 6D 1C F5 48 DC 43 EF 17 8B 08 AF 16 12 90 7A 8B 0A 3A E2 2C 2B CC 50 4A 10 EA 28 28 17 A7 E2 82 BC C5 44 39 FC 88 BF B7 8A 8A 2F 00 A0 FE A6 63 68 E7 AA 46 FD 04 3D 30 5F 88 B0 8A F1 61 29 06 22 8F 9E D2 91 F0 67 33 33 1C 00 00 01 40 20 08 10 2A 04 02 14 55 50 0A 05 54 15 28 81 22 24 FE 34 01 48 88 BC 44 67 F8 68 05 6B 5A C4 44 46 6F 14 88 8A 53 3B 6D DF EF D7 8A 74 51 DA 9B 18 2B 5F 7D F7 D3 A7 F1 10 0A C4 5A 28 42 A7 F0 55 01 85 F6 CE 73 9C C4 CF F0 70 0A CC CC 84 7C E8 8B FC 1D 50 A4 4A 21 18 B9 14 89 C3 A7 5E F8 29 16 0C 5C FB F6 DF BC DF 7D CD DF C2 40 29 4A 5F 33 11 5A D4 D1 81 D7 3C 83 B5 3F C6 00 26 22 33 21 1D 10 B5 CF BE E3 18 C0 A4 4A 11 A0 0C 1C 3A 35 60 4F C7 84 1C F9 C1 8B 05 D8 88 88 8A D7 EF 3A A7 1D 9D 36 06 B1 54 E1 97 01 18 70 16 34 44 26 3F 84 80 30 18 0E 07 03 82 F1 0F 06 05 61 C1 FC 30 03 51 68 91 2F 9B EF BF 7D 95 8B 04 11 38 32 BA F7 9A C5 81 22 B8 8A 71 DE E4 59 10 8A 79 2B 4A A1 50 A8 0C 0C C7 84 10 30 ED F8 3F 7C 0D 09 2F 34 FF 4F 01 04 0C FF 01 00 00 01 01 00 00 00 00 00 80 1F 00 00 B6 00 00 FF 5D 00 08 00 0F 00 12 00 05 EF FF 00 00 00 BC 01 00 00 01 00 00 FF 08 01 0F FF 00 02 80 1F 40 10 00 00 80 1F 80 1F 00 00 8A 13 1A 9A 80 1F 00 00 3E 23 00 00 00 00 01 B8 00 76 45 00 07 8F 51 00 1C 00 02 80 00 00 11 00 00 03 00 00 00 00 00 00 00 00 00 00 01 0E 0D 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 80 7F 00 04 06 FF 00 00 00 00 00 00 00 00 00 00 06 00 07 00 00 00 02 03 49 13 00 00 07 00 80 1A 06 00 00 09 00 00 FB FF 80 1A 06 00 49 0B 09 00 00 00 00 00 00 00
        # Arboria
        #E6 2D 84 12 4C 7F 14 C5 EF 98 AE 3E 04 D3 F1 B4 6F 8C F0 30 8B 61 04 19 13 5E 28 1B E0 61 15 C7 C4 C9 9A 36 79 C5 1E B1 3C CF 21 59 DF E4 F9 F2 65 EB 01 47 AC 40 66 36 8B 77 BB 8A 29 F4 21 15 EE 75 1B 46 FD BC 1A 11 6E E6 2B D9 F9 51 1B 46 FD BC 1A 11 6E EC E2 8A 7D 08 45 7B 3F AA A3 68 DC 2D C6 62 C1 6B 26 8D 11 4E F8 68 45 42 C3 E5 54 6C 6C 9A 9B A6 54 F2 03 53 CC 9B A6 4D D3 26 E9 97 34 CA 9E 64 DD 35 37 4E 8D D3 2E 69 02 39 A6 29 1B 46 FD 04 23 71 17 51 B8 93 88 B0 9B D7 06 7F 38 22 82 5F CE FF 53 F1 4F 9C 2F C1 D1 51 27 11 51 35 EF 15 14 A0 90 30 0A EB 50 0A 11 4C 6D 1C F5 48 DC 43 EF 17 8B 08 AF 16 12 90 7A 8B 0A 3A E2 2C 2B CC 50 4A 10 EA 28 28 17 A7 E2 82 BC C5 44 39 FC 88 BF B7 8A 8A 2F 00 A0 FE A6 63 68 E7 AA 46 FD 04 3D 30 5F 88 B0 8A F1 61 29 06 22 8F 9E D2 91 F0 67 33 33 1C 00 00 01 40 20 08 10 2A 04 02 14 55 50 0A 05 54 15 28 81 22 24 FE 34 01 48 88 BC 44 67 F8 68 05 6B 5A C4 44 46 6F 14 88 8A 53 3B 6D DF EF D7 8A 74 51 DA 9B 18 2B 5F 7D F7 D3 A7 F1 10 0A C4 5A 28 42 A7 F0 55 01 85 F6 CE 73 9C C4 CF F0 70 0A CC CC 84 7C E8 8B FC 1D 50 A4 4A 21 18 B9 14 89 C3 A7 5E F8 29 16 0C 5C FB F6 DF BC DF 7D CD DF C2 40 29 4A 5F 33 11 5A D4 D1 81 D7 3C 83 B5 3F C6 00 26 22 33 21 1D 10 B5 CF BE E3 18 C0 A4 4A 11 A0 0C 1C 3A 35 60 4F C7 84 1C F9 C1 8B 05 D8 88 88 8A D7 EF 3A A7 1D 9D 36 06 B1 54 E1 97 01 18 70 16 34 44 26 3F 84 80 30 18 0E 07 03 82 F1 0F 06 05 61 C1 FC 30 03 51 68 91 2F 9B EF BF 7D 95 8B 04 11 38 32 BA F7 9A C5 81 22 B8 8A 71 DE E4 59 10 8A 79 2B 4A A1 50 A8 0C 0C C7 84 10 30 ED F8 3F
        # Tarjan 1
        #E6 2D 84 12 4C 7F 14 C5 EF 98 AE 3E 04 D3 F1 B4 6F 8C F0 30 8B 61 04 19 13 5E 28 1B E0 61 15 C7 C4 C9 9A 36 79 C5 1E B1 3C CF 21 59 DF E4 F9 F2 65 EB 01 47 AC 40 66 36 8B 77 BB 8A 29 F4 21 15 EE 75 1B 46 FD BC 1A 11 6E E6 2B D9 F9 51 1B 46 FD BC 1A 11 6E EC E2 8A 7D 08 45 7B 3F AA A3 68 DC 2D C6 62 C1 6B 26 8D 11 4E F8 68 45 42 C3 E5 54 6C 6C 9A 9B A6 54 F2 03 53 CC 9B A6 4D D3 26 E9 97 34 CA 9E 64 DD 35 37 4E 8D D3 2E 69 02 39 A6 29 1B 46 FD 04 23 71 17 51 B8 93 88 B0 9B D7 06 7F 38 22 82 5F CE FF 53 F1 4F 9C 2F C1 D1 51 27 11 51 35 EF 15 14 A0 90 30 0A EB 50 0A 11 4C 6D 1C F5 48 DC 43 EF 17 8B 08 AF 16 12 90 7A 8B 0A 3A E2 2C 2B CC 50 4A 10 EA 28 28 17 A7 E2 82 BC C5 44 39 FC 88 BF B7 8A 8A 2F 00 A0 FE A6 63 68 E7 AA 46 FD 04 3D 30 5F 88 B0 8A F1 61 29 06 22 8F 9E D2 91 F0 67 33 33 1C 00 00 01 40 20 08 10 2A 04 02 14 55 50 0A 05 54 15 28 81 22 24 FE 34 01 48 88 BC 44 67 F8 68 05 6B 5A C4 44 46 6F 14 88 8A 53 3B 6D DF EF D7 8A 74 51 DA 9B 18 2B 5F 7D F7 D3 A7 F1 10 0A C4 5A 28 42 A7 F0 55 01 85 F6 CE 73 9C C4 CF F0 70 0A CC CC 84 7C E8 8B FC 1D 50 A4 4A 21 18 B9 14 89 C3 A7 5E F8 29 16 0C 5C FB F6 DF BC DF 7D CD DF C2 40 29 4A 5F 33 11 5A D4 D1 81 D7 3C 83 B5 3F C6 00 26 22 33 21 1D 10 B5 CF BE E3 18 C0 A4 4A 11 A0 0C 1C 3A 35 60 4F C7 84 1C F9 C1 8B 05 D8 88 88 8A D7 EF 3A A7 1D 9D 36 06 B1 54 E1 97 01 18 70 16 34 44 26 3F 84 80 30 18 0E 07 03 82 F1 0F 06 05 61 C1 FC 30 03 51 68 91 2F 9B EF BF 7D 95 8B 04 11 38 32 BA F7 9A C5 81 22 B8 8A 71 DE E4 59 10 8A 79 2B 4A A1 50 A8 0C 0C C7 84 10 30 ED F8 3F 7C 0D 09 2F 34 FF 4F 01 04 0C FF 01 00 00 01 01 00 00 00 00 00 80 1F 00 00 B6 00 00 FF 5D 00 08 00
        # Skara Brae (
        #E6 2D 84 12 4C 7F 14 C5 EF 98 AE 3E 04 D3 F1 B4 6F 8C F0 30 8B 61 04 19 13 5E 28 1B E0 61 15 C7 C4 C9 9A 36 79 C5 1E B1 3C CF 21 59 DF E4 F9 F2 65 EB 01 47 AC 40 66 36 8B 77 BB 8A 29 F4 21 15 EE 75 1B 46 FD BC 1A 11 6E E6 2B D9 F9 51 1B 46 FD BC 1A 11 6E EC E2 8A 7D 08 45 7B 3F AA A3 68 DC 2D C6 62 C1 6B 26 8D 11 4E F8 68 45 42 C3 E5 54 6C 6C 9A 9B A6 54 F2 03 53 CC 9B A6 4D D3 26 E9 97 34 CA 9E 64 DD 35 37 4E 8D D3 2E 69 02 39 A6 29 1B 46 FD 04 23 71 17 51 B8 93 88 B0 9B D7 06 7F 38 22 82 5F CE FF 53 F1 4F 9C 2F C1 D1 51 27 11 51 35 EF 15 14 A0 90 30 0A EB 50 0A 11 4C 6D 1C F5 48 DC 43 EF 17 8B 08 AF 16 12 90 7A 8B 0A 3A E2 2C 2B CC 50 4A 10 EA 28 28 17 A7 E2 82 BC C5 44 39 FC 88 BF B7 8A 8A 2F 00 A0 FE A6 63 68 E7 AA 46 FD 04 3D 30 5F 88 B0 8A F1 61 29 06 22 8F 9E D2 91 F0 67 33 33 1C 00 00 01 40 20 08 10 2A 04 02 14 55 50 0A 05 54 15 28 81 22 24 FE 34 01 48 88 BC 44 67 F8 68 05 6B 5A C4 44 46 6F 14 88 8A 53 3B 6D DF EF D7 8A 74 51 DA 9B 18 2B 5F 7D F7 D3 A7 F1 10 0A C4 5A 28 42 A7 F0 55 01 85 F6 CE 73 9C C4 CF F0 70 0A CC CC 84 7C E8 8B FC 1D 50 A4 4A 21 18 B9 14 89 C3 A7 5E F8 29 16 0C 5C FB F6 DF BC DF 7D CD DF C2 40 29 4A 5F 33 11 5A D4 D1 81 D7 3C 83 B5 3F C6 00 26 22 33 21 1D 10 B5 CF BE E3 18 C0 A4 4A 11 A0 0C 1C 3A 35 60 4F C7 84 1C F9 C1 8B 05 D8 88 88 8A D7 EF 3A A7 1D 9D 36 06 B1 54 E1 97 01 18 70 16 34 44 26 3F 84 80 30 18 0E 07 03 82 F1 0F 06 05 61 C1 FC 30 03 51 68 91 2F 9B EF BF 7D 95 8B 04 11 38 32 BA F7 9A C5 81 22 B8 8A 71 DE E4 59 10 8A 79 2B 4A A1 50 A8 0C 0C C7 84 10 30 ED F8 3F 7C 0D 09
        # Wilderness
        #E6 2D 84 12 4C 7F 14 C5 EF 98 AE 3E 04 D3 F1 B4 6F 8C F0 30 8B 61 04 19 13 5E 28 1B E0 61 15 C7 C4 C9 9A 36 79 C5 1E B1 3C CF 21 59 DF E4 F9 F2 65 EB 01 47 AC 40 66 36 8B 77 BB 8A 29 F4 21 15 EE 75 1B 46 FD BC 1A 11 6E E6 2B D9 F9 51 1B 46 FD BC 1A 11 6E EC E2 8A 7D 08 45 7B 3F AA A3 68 DC 2D C6 62 C1 6B 26 8D 11 4E F8 68 45 42 C3 E5 54 6C 6C 9A 9B A6 54 F2 03 53 CC 9B A6 4D D3 26 E9 97 34 CA 9E 64 DD 35 37 4E 8D D3 2E 69 02 39 A6 29 1B 46 FD 04 23 71 17 51 B8 93 88 B0 9B D7 06 7F 38 22 82 5F CE FF 53 F1 4F 9C 2F C1 D1 51 27 11 51 35 EF 15 14 A0 90 30 0A EB 50 0A 11 4C 6D 1C F5 48 DC 43 EF 17 8B 08 AF 16 12 90 7A 8B 0A 3A E2 2C 2B CC 50 4A 10 EA 28 28 17 A7 E2 82 BC C5 44 39 FC 88 BF B7 8A 8A 2F 00 A0 FE A6 63 68 E7 AA 46 FD 04 3D 30 5F 88 B0 8A F1 61 29 06 22 8F 9E D2 91 F0 67 33 33 1C 00 00 01 40 20 08 10 2A 04 02 14 55 50 0A 05 54 15 28 81 22 24 FE 34 01 48 88 BC 44 67 F8 68 05 6B 5A C4 44 46 6F 14 88 8A 53 3B 6D DF EF D7 8A 74 51 DA 9B 18 2B 5F 7D F7 D3 A7 F1 10 0A C4 5A 28 42 A7 F0 55 01 85 F6 CE 73 9C C4 CF F0 70 0A CC CC 84 7C E8 8B FC 1D 50 A4 4A 21 18 B9 14 89 C3 A7 5E F8 29 16 0C 5C FB F6 DF BC DF 7D CD DF C2 40 29 4A 5F 33 11 5A D4 D1 81 D7 3C 83 B5 3F C6 00 26 22 33 21 1D 10 B5 CF BE E3 18 C0 A4 4A 11 A0 0C 1C 3A 35 60 4F C7 84 1C F9 C1 8B 05 D8 88 88 8A D7 EF 3A A7 1D 9D 36 06 B1 54 E1 97 01 18 70 16 34 44 26 3F 84 80 30 18 0E 07 03 82 F1 0F 06 05 61 C1 FC 30 03 51 68 91 2F 9B EF BF 7D 95 8B 04 11 38 32 BA F7 9A C5 81 22 B8 8A 71 DE E4 59 10 8A 79 2B 4A A1 50 A8 0C 0C C7 84 10 30 ED F8 3F 7C 0D 09

        # 143618 is key
        mm.seek(143618)
        mm.read(1)  # FF - Throwaway
        dungeon_name_maybe = mm.read(1)
        dungeon_check_maybe = mm.read(1)    # Possibly the monster level?
        mm.read(1)  # Possibly wall type? But wilderness and gelidia are the same
        mm.read(2)  # 0cff
        # Now at 143621
        #mm.seek(143623)
        #mm.read(1)  # FF - Throwaway
        dungeon_maybe2 = mm.read(1) # 00 - dungeon, 01 - not a dungeon?

        mm.seek(143625)
        party_xpos = mm.read(1) # N/S position
        party_ypos = mm.read(1) # E/W position (starting bottom-left as 0,0)
        party_dir = mm.read(1)
        dimension_maybe = mm.read(1)
        # Also must be an indicator of whether the dungeon is going down or up (e.g. valarians tower)
        # For access to some floors, do we have to have completed some tasks?
        dungeon_level_maybe = mm.read(1)  # 00 - level 1, 01 - level 2, etc, FF - not a dungeon, i.e. outside or town
        mm.read(10)  # 00 00 00 00 80 1f 00 00 b6 00
        mm.read(1)   # 00 or e8; e8 if last level of dungeon? lake palace is exception
        mm.read(5)
        mm.read(1)   # 0f or 3d; ed if last level of dungeon?
        # Though 09-arboria.d64 and 10-caeria.d64 don't quite seem to match this
        print 'Party is at pos ({0},{1}) facing {2}'.format(int(hexlify(party_xpos),16),
                                                            int(hexlify(party_ypos),16),
                                                            direction[int(hexlify(party_dir),16)])
        print 'Party is in dimension {0}'.format(dimensions[int(hexlify(dimension_maybe),16)])
        print 'Party is in Dungeon {0} check {1} (Level {2})'.format(int(hexlify(dungeon_name_maybe),16),
                                                                     int(hexlify(dungeon_check_maybe),16),
                                                                     int(hexlify(dungeon_level_maybe),16))


        mm.seek(start_save_roster)


        # 31 total characters - 7 party + 24 in camp?
        for pos in range(0,68):
            read_chars(mm)

