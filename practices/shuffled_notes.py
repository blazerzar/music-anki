"""A Python script for generating shuffled notes for practicing, e.g., notes
on the guitar (play each note on each string).

Usage:
    python practices/shuffled_notes.py number_of_notes [options]

Arguments:
    number_of_notes: number of notes to generate
    -N: do not include natural notes
    --flats: output flat notes as well
    --sharps: output sharp notes as well
    --text: display notes in the terminal
    --help: show script usage documentation

If both --flats and --sharps are specified, the output will contain both, but
not enharmonically equivalent notes at the same time, e.g., F# and Gb.

Keybindings:
    space: regenerate notes
    n: toggle natural notes
    b: toggle flats
    s: toggle sharps
    up arrow: increase number of notes
    down arrow: decrease number of notes
    q: quit the program
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


def number_of_notes(natural, flats, sharps):
    notes = 7 * natural
    notes += 5 * (flats or sharps)
    return notes


def main():
    if len(argv) < 2:
        print(__doc__, end='')
        exit(1)

    natural = True
    flats = False
    sharps = False
    text = False

    for arg in argv[1:]:
        flats = flats or arg == '--flats'
        sharps = sharps or arg == '--sharps'
        text = text or arg == '--text'
        natural = natural and arg != '-N'

        if arg == '--help':
            print(__doc__, end='')
            exit(0)

    num_notes = argv[1]
    if not num_notes.isdigit():
        print('The first argument must be a number.')
        exit(1)
    num_notes = int(num_notes)

    available = number_of_notes(natural, flats, sharps)
    if num_notes > available:
        print(f'Cannot generate {num_notes} notes, only {available} available.')
        exit(1)

    lines, rows, cols = create_output_lines(num_notes, natural, flats, sharps)

    if text:
        for i in range(rows):
            left = lines[i].strip()
            right = lines[i + rows] if i + rows < len(lines) else ''
            if not right:
                print(left)
            else:
                print(f'{left:<8} {right}')
    else:
        import matplotlib.pyplot as plt

        plt.rcParams['toolbar'] = 'None'
        fig, ax = plt.subplots()
        fig.canvas.manager.set_window_title('Shuffled Notes')

        def on_key(event):
            nonlocal num_notes, natural, flats, sharps

            natural = not natural if event.key == 'n' else natural
            flats = not flats if event.key == 'b' else flats
            sharps = not sharps if event.key == 's' else sharps
            if not any((natural, flats, sharps)):
                natural = True

            num_notes += (event.key == 'up') - (event.key == 'down')
            available = number_of_notes(natural, flats, sharps)
            num_notes = max(1, min(num_notes, available))

            need_redraw = event.key in (' ', 'up', 'down', 'n', 'b', 's')
            if need_redraw:
                args = create_output_lines(num_notes, natural, flats, sharps)
                ax.cla()
                render(*args, fig, ax)
                plt.draw()

        fig.canvas.mpl_connect('key_press_event', on_key)

        render(lines, rows, cols, fig, ax)
        plt.show()


def create_output_lines(num_notes, natural, flats, sharps):
    """Samples num_notes from note_indices and formats them into an enumerated
    list. If accidentals are included, they are written as sharps or flats,
    depending on the configuration."""

    note_indices = []
    if natural:
        note_indices += [0, 1, 2, 3, 4, 5, 6]
    if flats or sharps:
        note_indices += [7, 8, 9, 10, 11]

    selected_notes = sample(note_indices, num_notes)
    output = ''
    for i, note in enumerate(selected_notes):
        if note < 7:
            out = notes[note][0]
        elif flats and sharps:
            out = sample(notes[note], 1)[0]
        elif flats:
            out = notes[note][1]
        elif sharps:
            out = notes[note][0]
        output += f'{i + 1:>2}. {out}\n'

    # Format the output into two columns with a maximum of 6 notes per column
    output = output.rstrip()
    cols = 1 if num_notes <= 6 else 2
    rows = (num_notes // cols) + (num_notes % cols > 0)
    lines = output.split('\n')

    return lines, rows, cols


def render(lines, rows, cols, fig, ax):
    fig.set_figwidth(2.2 if cols == 1 else 5.5)
    fig.set_figheight(rows * 0.9)

    # Left column can be stripped because numbers are always 1 digit
    left_col = [line.strip() for line in lines[:rows]]
    right_col = lines[rows:]

    # Add padding to allow using ha='center'
    left_max = max(len(line) for line in left_col)
    left_col = '\n'.join(line.ljust(left_max) for line in left_col)
    if right_col:
        right_max = max(len(line) for line in right_col)
        # Pad right column to allow using va='center'
        right_col += [''] * (rows - len(right_col))
        right_col = '\n'.join(line.ljust(right_max) for line in right_col)

    kwargs = {
        'ha': 'center',
        'va': 'center',
        'fontsize': 45,
        'linespacing': 1.6,
        'fontfamily': 'monospace',
    }

    ax.text(0.5 if cols == 1 else 0.1, 0.5, left_col, **kwargs)
    if right_col:
        ax.text(0.82, 0.5, right_col, **kwargs)
    ax.axis('off')


if __name__ == '__main__':
    main()
