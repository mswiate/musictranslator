from random import choice


class RhythmMaker:
    # in case of 'dynamic' rhythm arg don't need to make crazy asd table
    def __init__(self, option):
        self.size = 32
        if option == 'dynamic':
            self.rhythm_array = self.__set_rhythm_array()
        else:
            self.rhythm_array = {}

    # makes crazy asd table in purpose to match notes durations to 1/2^n pattern
    # A - filled with false
    # A(0,0) = true
    # A(time, letter) = at least for one of notes 1..32 A(time - note_dur, letter - 1) is true? true : false
    # it uses list because its easier to take information from table later
    def __set_rhythm_array(self):
        r_array = [[[] for x in range(self.size + 1)] for y in range(self.size + 1)]
        r_array[0][0].append(0)

        for note_no in range(1, self.size + 1):
            for time in range(1, self.size + 1):
                for note in [2 ** n for n in range(0, 6)]:
                    if time - note >= 0 and r_array[time - note][note_no - 1]:
                        r_array[time][note_no].append(note)

        return r_array

    # gives rhythm to tact (it returns array of note durations)
    def tact_rhythm(self, letters_no):
        if letters_no > self.size or not self.rhythm_array:
            return self.__tact_rhythm_cut(letters_no)
        tact = []
        time = self.size
        letter = letters_no
        min_note = self.__min_note(letters_no)

        while letter != 0:
            notes_list = self.rhythm_array[time][letter]
            # better choice get rid off short notes - it gives better sound
            better_choice = [n for n in notes_list if n >= min_note]
            note = choice(better_choice if better_choice else notes_list)
            tact.append(note)
            time -= note
            letter -= 1
        return [float(2 * n) / float(self.size) for n in tact]

    # in case of uninteresting choice named: "cut" there are such patterns as below
    def __tact_rhythm_cut(self, letters_no):
        if letters_no < 2:
            return [2.0]
        elif letters_no < 4:
            return [1.0, 1.0]
        elif letters_no < 8:
            return [0.5, 0.5, 0.5, 0.5]
        elif letters_no < 16:
            return [0.25 for i in range(8)]
        elif letters_no < 32:
            return [0.125 for i in range(16)]
        else:
            return [0.0625 for i in range(32)]

    # gives minimum note duration that should be used - we dont like short notes
    def __min_note(self, word_length):
        if word_length == 1:
            return 32
        if word_length == 2:
            return 16
        if word_length <= 4:
            return 8
        if word_length <= 8:
            return 4
        if word_length <= 16:
            return 2
        if word_length <= 32:
            return 1
