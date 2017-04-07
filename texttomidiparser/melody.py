# scales
MINOR = [84, 86, 87, 89, 91, 92, 94, 96]
MAJOR = [84, 86, 88, 89, 91, 93, 95, 96]
scale_C = 84


# damn U UTF-8
def is_vowel(letter):
    return letter in 'aeiuoyąęóàâáåäãąæœðéêëęěîìíïıòöôóøùúûüůý'


class Song:
    def __init__(self, velocity, notes_dict, chord_maker, rhythm_maker):
        self.tacts = []
        self.velocity = velocity
        self.notes_dict = notes_dict
        self.chord_maker = chord_maker
        self.rhythm_maker = rhythm_maker

    def add_tact(self, word):
        self.tacts.append(Tact(word, self.velocity, self.notes_dict, self.rhythm_maker))

    def print(self):
        song = []
        time = 0.0
        for tact in self.tacts:
            printed_tact = tact.print(time)
            song.extend(printed_tact)
            song.extend(self.chord_maker.make_chords(time, printed_tact))
            time += 2.0
        return song


class Tact:
    def __init__(self, word, velocity, notes_dict, rhythm_maker):
        self.word = word
        self.velocity = velocity
        self.notes_dict = notes_dict
        self.rhythm_maker = rhythm_maker
        self.rhythm = self.rhythm_maker.tact_rhythm(len(word))

    def print(self, time):
        tact = []
        curr = 0  # current letter
        for letter_time in self.rhythm:
            letter = self.word[curr].lower()
            if letter in self.notes_dict.keys():
                tact.append([time, self.notes_dict[letter], self.velocity,
                             2.0 * letter_time if is_vowel(letter) else letter_time])  # vowels are longer
            time += letter_time
            curr += 1
        return tact
