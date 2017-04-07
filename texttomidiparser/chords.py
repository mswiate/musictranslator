from random import randint

from texttomidiparser.melody import scale_C

# for float eq
EPS = 0.001
CHORD_TRANS = 36


def eq(a, b):
    return abs(a - b) < EPS


# chords are made like this:
# 1. find patterns:
#  if it can make chord pattern(1, 2, 4)- that means that every chord will be played in the same time as note
# 2. choose pattern - it choose from posibble paterns by shear luck modified with argument (sparseness)
# 3. build chord for each place in pattern: chord are build on the note played
class ChordMaker:
    def __init__(self, scale, velocity, sparseness):
        self.scale = scale
        self.velocity = velocity
        self.spr = sparseness
        self.chord_dur = 0.7

    # it makes chord depending on tact
    def make_chords(self, time, tact):
        chords_pattern = self.__match_pattern(tact, time)
        chords = []
        for time in chords_pattern:
            note = [l for l in tact if eq(l[0], time)]
            if not note: # it should not happen
                return []
            chord_pitches = self.__find_chord(note[0][1])
            for pitch in chord_pitches:
                chords.append([time, pitch, self.velocity, self.chord_dur])
        return chords

    # it finds pattern for chord - in the way described above
    def __match_pattern(self, tact, time):
        note1 = [l for l in tact if eq(l[0], time)]
        note2 = [l for l in tact if eq(l[0], time + 0.5)]
        note3 = [l for l in tact if eq(l[0], time + 1.0)]
        note4 = [l for l in tact if eq(l[0], time + 1.5)]
        if note1 and note2 and note3 and note4 and randint(0, self.spr) == 0:
            return [time, time + 0.5, time + 1.0, time + 1.5]
        elif note1 and note3 and randint(0, self.spr // 2) == 0:
            return [time, time + 1.0]
        else:
            return [time]

    # it makes notes for chord that is built in __build_chord
    def __find_chord(self, note):
        scale_note = (note % 12) + scale_C  # to adjust to scale from melody.scales
        pos = self.scale.index(scale_note)
        return [self.scale[n] - CHORD_TRANS for n in self.__build_chord(pos)]

    # pos - note position in scale
    def __build_chord(self, pos):
        if randint(0, 2) == 0 and 5 >= pos >= 2:
            return [pos - 2, pos, pos + 2]
        elif pos < 4:
            return [pos, pos + 2, pos + 4]
        else:
            return [pos - 4, pos - 2, pos]
