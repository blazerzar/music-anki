"""
Create an Anki deck for naming notes and their scale degrees in guitar chords.
"""

from os import mkdir, path, remove, rmdir

import genanki
import matplotlib.pyplot as plt

from utils import card_model, chord_diagram, note_to_latex

CHORDS_FILE = path.join('data', 'chords.csv')
TEMP_DIR = 'temp_guitar_chord_notes'
OUTPUT_DIR = 'out'


def main():
    if not path.exists(OUTPUT_DIR):
        mkdir(OUTPUT_DIR)
    if not path.exists(TEMP_DIR):
        mkdir(TEMP_DIR)

    chords = load_chords(CHORDS_FILE)

    media_files = []
    deck = genanki.Deck(
        1541482719,
        'Music::Guitar Chord Notes',
    )

    table_style = 'style="margin-left: auto; margin-right: auto; padding: 10px;"'

    for name, diagram, fingering, notes, degrees in chords:
        notes_table = f'<table {table_style}>'
        for row in [notes, degrees]:
            r = ''.join(f'<td>{note_to_latex(note)}</td>' for note in row.split())
            notes_table += f'<tr>{r}</tr>'
        notes_table += '</table>'

        fig, ax = chord_diagram(diagram, fingering, name, show_name=False)
        filename = path.join(TEMP_DIR, f'{name}.png')
        plt.xlim(-0.5, 5.5)
        plt.ylim(-0.1, 7.8)
        fig.savefig(filename, bbox_inches='tight')
        plt.close(fig)

        media_files.append(filename)

        note = genanki.Note(
            model=card_model,
            fields=[
                f'<img src="{name}.png" width="120px">',
                f'{note_to_latex(name)}<br>{notes_table}',
            ],
        )
        deck.add_note(note)

    package = genanki.Package(deck)
    package.media_files = media_files
    package.write_to_file(f'{OUTPUT_DIR}/guitar_chord_notes.apkg')

    for file in media_files:
        remove(file)
    rmdir(TEMP_DIR)


def load_chords(filename):
    chords = []
    names = set()
    with open(filename, 'r', encoding='utf-8') as f:
        next(f)
        for line in f:
            name, diagram, fingering, notes, degrees = line.strip().split(',')
            if name in names:
                continue

            chords.append((name, diagram, fingering, notes, degrees))
            names.add(name)
    return chords


if __name__ == '__main__':
    main()
