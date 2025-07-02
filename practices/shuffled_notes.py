"""A Python script for generating shuffled notes for practicing, e.g., notes
on the guitar (play each note on each string).

Usage:
    python practices/shuffled_notes.py number_of_notes [-N] [--flats] [--sharps]

Arguments:
    number_of_notes: number of notes to generate
    -N: do not include natural notes
    --flats: output flat notes as well
    --sharps: output sharp notes as well

If both --flats and --sharps are specified, the output will contain both, but
not enharmonically equivalent notes at the same time, e.g., F# and Gb.
"""

from random import sample
from sys import argv

notes = [
    ('A',),
    ('B',),
    ('C',),
    ('D',),
    ('E',),
    ('F',),
    ('G',),
    ('A#', 'Bb'),
    ('C#', 'Db'),
    ('D#', 'Eb'),
    ('F#', 'Gb'),
    ('G#', 'Ab'),
]


def main():
    if len(argv) < 2:
        print(__doc__, end='')
        exit(1)

    num_notes = argv[1]
    if not num_notes.isdigit():
        print('The first argument must be a number.')
        exit(1)
    num_notes = int(num_notes)

    note_indices = [0, 1, 2, 3, 4, 5, 6]
    flats = False
    sharps = False

    for arg in argv[2:]:
        flats = flats or arg == '--flats'
        sharps = sharps or arg == '--sharps'
        if arg == '-N':
            note_indices = []

    if flats or sharps:
        note_indices += [7, 8, 9, 10, 11]

    available = len(note_indices)
    if num_notes > available:
        print(f'Cannot generate {num_notes} notes, only {available} available.')
        exit(1)

    selected_notes = sample(note_indices, num_notes)
    for i, note in enumerate(selected_notes):
        if note < 7:
            out = notes[note][0]
        elif flats and sharps:
            out = sample(notes[note], 1)[0]
        elif flats:
            out = notes[note][1]
        elif sharps:
            out = notes[note][0]
        print(out, end=' ' if i < num_notes - 1 else '\n')


if __name__ == '__main__':
    main()
