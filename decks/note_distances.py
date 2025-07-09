"""
Create a deck for learning the number of note letters between two notes, e.g.,
between C and F the distance is 4 (C, D, E, F).
"""

from os import path

import genanki

from utils import card_model

OUTPUT_DIR = 'out'


def main():
    deck = genanki.Deck(1312897177, 'Music::Note Distances')
    notes = 'CDEFGAB'

    for i, start in enumerate(notes):
        for j, end in enumerate(notes):
            if i == j:
                continue
            if j < i:
                j += len(notes)

            note = genanki.Note(
                model=card_model,
                fields=[
                    f'Distance between {start} and {end}?',
                    str(j - i + 1),
                ],
            )
            deck.add_note(note)

    package = genanki.Package(deck)
    package.write_to_file(path.join(OUTPUT_DIR, 'note_distances.apkg'))


if __name__ == '__main__':
    main()
