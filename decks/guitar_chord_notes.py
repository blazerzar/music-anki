"""
Creates an Anki deck for naming notes and their scale degrees in guitar chords.
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
        prefix = 'ukulele'
    else:
        chords = load_chords(GUITAR_CHORDS)
        deck = genanki.Deck(1541482719, 'Music::Guitar Chord Notes')
        out_file = path.join(OUTPUT_DIR, 'guitar_chord_notes.apkg')
        prefix = 'guitar'

    # Remove duplicate chords with different fingerings
    chords = {
        ' '.join(str(d) if d is not None else 'x' for d in chord.diagram): chord
        for chord in chords
    }
    chords = list(chords.values())

    media_files = []
    table_style = 'style="margin-left: auto; margin-right: auto; padding: 10px;"'

    for chord in chords:
        notes_table = f'<table {table_style}>'
        for row, f in [(chord.notes, note_to_latex), (chord.degrees, degree_to_latex)]:
            r = ''.join(f'<td>{f(note)}</td>' for note in row if note != 'x')
            notes_table += f'<tr>{r}</tr>'
        notes_table += '</table>'

        fig, ax = plt.subplots(figsize=(4, 6))
        chord_diagram(chord, ax, show_name=False)
        name = chord.name.replace('/', '_')
        diagram = ''.join(str(d) if d is not None else 'x' for d in chord.diagram)
        filename = f'{prefix}_{name}_{diagram}.png'
        filepath = path.join(TEMP_DIR, filename)
        plt.savefig(filepath, bbox_inches='tight')
        plt.close()

        media_files.append(filepath)

        note = genanki.Note(
            model=card_model,
            fields=[
                f'<img src="{filename}" width="150px">',
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
