"""
Create an Anki deck for naming notes and their scale degrees in guitar chords.
"""

from os import mkdir, path, remove, rmdir

import genanki
import matplotlib.pyplot as plt

from anki.utils import card_model, note_to_latex

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

    for name, diagram, notes, degrees in chords:
        notes_table = f'<table {table_style}>'
        for row in [notes, degrees]:
            r = ''.join(f'<td>{note_to_latex(note)}</td>' for note in row.split())
            notes_table += f'<tr>{r}</tr>'
        notes_table += '</table>'

        filename = chord_diagram(diagram, name)
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
    """Load chords data from a CSV file. For this deck, fingering is ignored."""
    chords = []
    names = set()
    with open(filename, 'r', encoding='utf-8') as f:
        next(f)
        for line in f:
            name, diagram, notes, degrees, _ = line.strip().split(',')
            if name in names:
                continue

            chords.append((name, diagram, notes, degrees))
            names.add(name)
    return chords


def chord_diagram(diagram, name):
    fig, ax = plt.subplots(figsize=(4, 6))

    ax.add_patch(plt.Rectangle((0, 0), 5, 7, ec='black', fc='white', lw=1.5))
    # Strings
    for x in range(4):
        ax.add_line(plt.Line2D([x + 1, x + 1], [0, 7], color='black', lw=1.5))
    # Frets
    for i in range(4):
        y = 7 * (i + 1) / 5
        ax.add_line(plt.Line2D([0, 5], [y, y], color='black', lw=1.5))
    # Nut
    ax.add_line(plt.Line2D([0.04, 4.96], [7, 7], color='black', lw=4))

    for string, fret in enumerate(diagram):
        if fret == 'x' or fret == '0':
            args = string, 7.4, 160
            m = 'x' if fret == 'x' else 'o'
            kwargs = (
                {'c': 'black'}
                if fret == 'x'
                else {'edgecolor': 'black', 'facecolor': 'white'}
            )
            plt.scatter(*args, marker=m, **kwargs, lw=2.2)
        else:
            fret = int(fret)
            y = 7.7 - 7 * fret / 5
            x = string
            ax.add_patch(plt.Circle((x, y), 0.35, color='black'))

    plt.axis('equal')
    plt.axis('off')

    filename = path.join(TEMP_DIR, f'{name}.png')
    plt.savefig(filename, bbox_inches='tight')
    plt.close(fig)
    return filename


if __name__ == '__main__':
    main()
