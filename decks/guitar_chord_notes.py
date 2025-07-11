"""
Create an Anki deck for naming notes and their scale degrees in guitar chords.
"""

from os import mkdir, path, remove, rmdir
from sys import argv

import genanki
import matplotlib.pyplot as plt

from utils import (
    card_model,
    chord_diagram,
    chord_to_latex,
    degree_to_latex,
    load_chords,
    note_to_latex,
)

GUITAR_CHORDS = path.join('data', 'guitar_chords.csv')
UKULELE_CHORDS = path.join('data', 'ukulele_chords.csv')
TEMP_DIR = 'temp_guitar_chord_notes'
OUTPUT_DIR = 'out'


def main():
    if not path.exists(OUTPUT_DIR):
        mkdir(OUTPUT_DIR)
    if not path.exists(TEMP_DIR):
        mkdir(TEMP_DIR)

    if len(argv) > 1 and argv[1] == 'ukulele':
        chords = load_chords(UKULELE_CHORDS)
        deck = genanki.Deck(1440356293, 'Music::Ukulele Chord Notes')
        out_file = path.join(OUTPUT_DIR, 'ukulele_chord_notes.apkg')
        prefix = 'ukulele_'
    else:
        chords = load_chords(GUITAR_CHORDS)
        deck = genanki.Deck(1541482719, 'Music::Guitar Chord Notes')
        out_file = path.join(OUTPUT_DIR, 'guitar_chord_notes.apkg')
        prefix = 'guitar_'

    # Remove duplicate chords with different fingerings
    chords = list({chord.name: chord for chord in chords}.values())

    media_files = []
    table_style = 'style="margin-left: auto; margin-right: auto; padding: 10px;"'

    for chord in chords:
        notes_table = f'<table {table_style}>'
        for row, f in [(chord.notes, note_to_latex), (chord.degrees, degree_to_latex)]:
            r = ''.join(f'<td>{f(note)}</td>' for note in row)
            notes_table += f'<tr>{r}</tr>'
        notes_table += '</table>'

        fig, ax = plt.subplots(figsize=(4, 6))
        chord_diagram(chord, ax, show_name=False)
        filename = path.join(TEMP_DIR, f'{prefix}{chord.name}.png')
        plt.savefig(filename, bbox_inches='tight')

        media_files.append(filename)

        note = genanki.Note(
            model=card_model,
            fields=[
                f'<img src="{prefix}{chord.name}.png" width="150px">',
                f'{chord_to_latex(chord.name)}<br>{notes_table}',
            ],
        )
        deck.add_note(note)

    package = genanki.Package(deck)
    package.media_files = media_files
    package.write_to_file(out_file)

    for file in media_files:
        remove(file)
    rmdir(TEMP_DIR)


if __name__ == '__main__':
    main()
