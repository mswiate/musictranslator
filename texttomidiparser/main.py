from argparse import ArgumentParser

from miditime.miditime import MIDITime

from texttomidiparser.chords import ChordMaker
from texttomidiparser.lettersparse import Language, letter_notes_dict
from texttomidiparser.melody import MAJOR, MINOR, Song
from texttomidiparser.rhythm import RhythmMaker

args_parser = ArgumentParser(description="parse poems to melancholic, narcotic midi!")

args_parser.add_argument('--lang', type=Language, default="Polish",
                         help='languages: {}'.format(', '.join([lang.value for lang in Language])))
args_parser.add_argument('-o', type=str, help="output file name")
args_parser.add_argument('--poem', type=str, default="poems/staff.txt", help="a file with your poem")
args_parser.add_argument('--gama', type=int, choices=[1, 2], default=1, help='how wide (in octaves) the gama should be?')
args_parser.add_argument('--rhythm', type=str, choices=['cut', 'dynamic'],
                         default='cut', help='if you prefer brainwashing music choose dynamic')
args_parser.add_argument('--scale', choices=["MINOR", "MAJOR"], default="MINOR",
                         help='if happy choose minor, otherwise choose minor')
args_parser.add_argument('-l', action='store_true', help='if pitch is to high')
args_parser.add_argument('--chords', type=int, choices=[0, 1, 2, 3, 4, 5, 6, 7, 8],
                         default=2, help='higher int sparser chords')


def main():
    args = args_parser.parse_args()

    vel = 127
    scale = MINOR if args.scale == "MINOR" else MAJOR

    # opens file with poem to parse
    with open(args.poem, 'r', encoding="UTF-8") as poem:
        poem_lines = poem.readlines()

    letter_notes = letter_notes_dict(args.lang, args.gama, scale)

    # sometimes there is strange utf sig in the first spot
    if poem_lines[0][0].lower() not in letter_notes.keys():
        poem_lines[0] = poem_lines[0][1:]

    # lowers all notes if necessary
    if args.l:
        for letter, note in letter_notes.items():
            letter_notes[letter] = note - 12

    rhythm_maker = RhythmMaker(args.rhythm)
    chord_maker = ChordMaker(scale, vel // 2, args.chords)

    song = Song(vel, letter_notes, chord_maker, rhythm_maker)
    for line in poem_lines:
        for word in line.split():
            song.add_tact(word)

    mymidi = MIDITime(90, args.o)
    mymidi.add_track(song.print())

    mymidi.save_midi()
