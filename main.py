from midiutil import MIDIFile

from constants import (MIDI_NOTE_NUMBERS, SD)

track = 0
channel = 0
time = 0  # In beats
#duration = 1  # In beats
tempo = 80  # In BPM
volume = 100  # 0-127, as per the MIDI standard

number_of_tracks = 1

MyMIDI = MIDIFile(number_of_tracks)
MyMIDI.addTempo(track, time, tempo)


def get_midi_note_number(note):
    if note in MIDI_NOTE_NUMBERS.keys():
        return MIDI_NOTE_NUMBERS[note]
    elif note in MIDI_NOTE_NUMBERS.values():
        return note
    else:
        # TODO: detect same notes in different octaves
        raise ValueError('Invalid midi note')


class Scale:
    def __init__(self, root, scale_type='maj'):
        self.root = get_midi_note_number(root)
        if type not in self.scale_intervals.keys():
            raise ValueError('Invalid scale type')
        self.scale = [root]
        for interval in self.scale_intervals[scale_type]:
            self.scale.append(self.scale[-1] + interval)

    def chord(self, scale_degree, chord_type='maj'):
        return Chord(self.root + scale_degree, chord_type).chord

    @property
    def scale_intervals(self):
        # In semitones
        # TODO: add more
        return {
            'maj': [2, 2, 1, 2, 2, 2, 1],
            'min': [2, 1, 2, 2, 1, 2, 2],  # Natural minor
            'blues': [3, 2, 1, 1, 3, 2],
        }


class Chord:
    def __init__(self, root, chord_type='maj'):
        self._root = get_midi_note_number(root)
        self.chord = [(self._root + note) for note in self.chord_types[chord_type]]

    @property
    def chord_types(self):
        # Scale degrees of each chord
        return {
            'maj': [SD['1'], SD['3'], SD['5']],
            'min': [SD['1'], SD['flat 3'], SD['5']],
            '7': [SD['1'], SD['3'], SD['5'], SD['flat 7']],
            'maj7': [SD['1'], SD['3'], SD['5'], SD['flat 7']],
            'min7': [SD['1'], SD['flat 3'], SD['5'], SD['flat 7']],
            '5': [SD['1'], SD['5']]
        }

    def play(self, start_time, duration):
        for pitch in self.chord:
            Note(pitch, start_time, duration).play()


class Note:
    def __init__(self, pitch, start_time, duration, track_number=0, volume=100):
        self.pitch = pitch
        self.start_time = start_time
        self.duration = duration
        self.track_number = track_number
        self.volume = volume

    def play(self):
        if self.start_time in tracks[self.track_number].keys():
            print("TRY" + str(self.pitch))
            tracks[self.track_number][self.start_time] += [self]
        else:
            print("KEY" + str(self.pitch))
            tracks[self.track_number][self.start_time] = [self]
        MyMIDI.addNote(track, channel, self.pitch, self.start_time, self.duration, self.volume)


tracks = [dict(list())] * number_of_tracks

def repeat(track_number, duration, start_repeat, start=0 ):
    end = start + duration
    for track_time in tracks[track_number].copy().keys():
        if start <= track_time <= end:
            for note in tracks[track_number][track_time]:
                copied_note = note
                copied_note.start_time = start_repeat + (track_time - start)
                copied_note.play()


with open("franzs_masterpiece.mid", "wb") as output_file:
    MyMIDI.writeFile(output_file)

