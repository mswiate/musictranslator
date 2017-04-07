from enum import Enum
from operator import itemgetter


class Language(Enum):
    EN = "English"
    FR = "French"
    GE = "German"
    ES = "Spanish"
    PR = "Portuguese"
    IT = "Italian"
    TU = "Turkish"
    SW = "Swedish"
    PL = "Polish"
    DU = "Dutch"
    DA = "Danish"
    IC = "Icelandic"
    FI = "Finnish"
    CZ = "Czech"


# makes what it says- depending on letter frequency in given language:
# higher frequency gives higher frequency in music- lower gives lower
# gama is for number of octaves
def letter_notes_dict(language, gama, scale):
    rscale = scale[::-1]  # its easier to use reversed note range

    # if we have two octaves:
    notes_range = rscale[:-1:] + [x - 12 for x in rscale] if gama == 2 else rscale

    # it sorts letter to its freq in language in desc order by freq
    letter_freq = sorted(letter_freq_dict(language).items(), key=itemgetter(1), reverse=-1)
    letter_note = {}

    curr = 0  # current note in notes range
    note_gap = 100.0 / float(len(notes_range))  # how many frequencies for one note
    gap_fill = 0.0  # how much gap is filled
    total = 0.0  # dont know why but frequencies in some langs sum up to more than 100% (uber german)

    # 0..n letters for one gap; one note for one gap
    for letter, freq in letter_freq:
        gap_fill += freq  # we fill gap
        total += freq
        if total > 100.0:  # in case of bad letterfreq we gives rest letters to the lowest note
            letter_note[letter] = notes_range[curr]
        elif gap_fill < note_gap:
            letter_note[letter] = notes_range[curr]
        else:  # if it is to much for this gap we search till it dont fill in gap
            while gap_fill > note_gap:
                gap_fill -= note_gap
                curr += 1
            letter_note[letter] = notes_range[curr]

    return letter_note


# maps letters from letterfreq file to its frequencies in language
def letter_freq_dict(language):
    with open('data/letterfreq', "r", encoding='UTF-8') as f:
        lines = f.readlines()

    row_no = lines[0].split().index(language.value)
    letter_word = lines[0].split()[0]
    letter_freq = {}

    for line in lines:
        split_line = line.split()
        if split_line[0] != letter_word and split_line[row_no] != '0':
            letter_freq[split_line[0]] = float(split_line[row_no].strip('%'))

    return letter_freq
