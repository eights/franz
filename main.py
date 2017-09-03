from midiutil import MIDIFile

from constants import *

track = 0
channel = 0
time = 0    # In beats
duration = 1    # In beats
tempo = 80   # In BPM
volume = 100  # 0-127, as per the MIDI standard

MyMIDI = MIDIFile(1)  # One track, defaults to format 1 (tempo track is created
                      # automatically)
MyMIDI.addTempo(track, time, tempo)


def get_midi_note_number(note):
    if note in MIDI_NOTE_NUMBERS.keys():
        return MIDI_NOTE_NUMBERS[note]
    elif note in MIDI_NOTE_NUMBERS.values():
        return note
    else:
        # TODO: detect same notes in different octaves
        raise ValueError('Invalid midi note')


class ScaleBuilder:
    def __init__(self, root, scale_type='maj'):
        self.root = get_midi_note_number(root)
        if type not in self.scale_intervals.keys():
            raise ValueError('Invalid scale type')
        self.scale = [root]
        for interval in self.scale_intervals[scale_type]:
            self.scale.append(self.scale[-1] + interval)

    @property
    def scale_intervals(self):
        # In semitones
        # TODO: add more scales
        return {
            'maj': [2, 2, 1, 2, 2, 2, 1],
            'min': [2, 1, 2, 2, 1, 2, 2],  # Natural minor
            'blues': [3, 2, 1, 1, 3, 2],
        }


class ChordBuilder:
    def __init__(self, root):
        self.root = get_midi_note_number(root)

    @property
    def chord_notes(self):
        # Scale degrees of each chord
        return {
            'maj': [SD_1, SD_3, SD_5],
            'min': [SD_1, SD_FLAT_3, SD_5],
            '7': [SD_1, SD_3, SD_5, SD_FLAT_7],
            'maj7': [SD_1, SD_3, SD_5, SD_7],
            'min7': [SD_1, SD_FLAT_3, SD_5, SD_FLAT_7],
            '5': [SD_1, SD_5]
        }


def add_note(pitch, i, duration, track=0):
    MyMIDI.addNote(track, channel, pitch, time + i, duration, volume)


with open("franzs_masterpiece.mid", "wb") as output_file:
    MyMIDI.writeFile(output_file)
