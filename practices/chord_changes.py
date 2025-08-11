"""A Python script for sampling random chords for practicing changing between
them.

Usage:
    python practices/chord_changes.py [ukulele|chords csv file path] [options]

Examples:
    python practices/chord_changes.py -n 3
    python practices/chord_changes.py ukulele
    python practices/chord_changes.py my_chords.csv --chords 10 -n 4
    python practices/chord_changes.py --include data/bar_chords.csv
    python practices/chord_changes.py --include "F(1 3 3 2 1 1),B"

Arguments:
    --chords num: number of chord samples, by default, all chords are used
    -n num: chord sample size, default is 2
    --include tag: include only chords in the specified tag file
    --exclude tag: exclude chords in the specified tag file
    --help: show script usage documentation

Instead of a tag file, a comma-separated list of chords can be specified. If
multiple chords with the same name exist, using just a name corresponds to all
of them. To specify a single ambiguous chord, the diagram can be written in
the parentheses.

Keybindings:
    space: show next sample of chords
    q: quit the program
"""

import sys
from os import path
from random import shuffle

import matplotlib.pyplot as plt

sys.path.append(path.join(path.dirname(path.abspath(__file__)), '..'))
from utils import Chord, chord_diagram, load_chords

GUITAR_CHORDS = path.join('data', 'guitar_chords.csv')
UKULELE_CHORDS = path.join('data', 'ukulele_chords.csv')


def main():
    chords_file = GUITAR_CHORDS
    num_chords = None
    sample_size = 2

    include, exclude = [], []

    for i, arg in enumerate(sys.argv):
        if arg == '--chords' and i + 1 < len(sys.argv):
            num_chords = int(sys.argv[i + 1])
        elif arg == '-n' and i + 1 < len(sys.argv):
            sample_size = int(sys.argv[i + 1])
        elif arg == '--help':
            print(__doc__, end='')
            exit(0)
        elif arg == '--include' and i + 1 < len(sys.argv):
            include = parse_tag(sys.argv[i + 1])
        elif arg == '--exclude' and i + 1 < len(sys.argv):
            exclude = parse_tag(sys.argv[i + 1])
        elif i == 1 and arg == 'ukulele':
            chords_file = UKULELE_CHORDS
        elif i == 1 and arg.endswith('.csv'):
            chords_file = arg

    chords = load_chords(chords_file)
    chords = filter_chords(chords, include, exclude)
    if num_chords is None:
        num_chords = len(chords)

    samples = num_chords // sample_size

    plt.rcParams['toolbar'] = 'None'
    width = (3.3 if len(chords[0].diagram) == 6 else 2.5) * sample_size
    fig, ax = plt.subplots(1, sample_size, figsize=(width, 5.4))
    fig.canvas.manager.set_window_title('Chord Changes')
    if sample_size == 1:
        ax = [ax]

    counter = fig.text(0.5, 0.07, '', fontsize=9, ha='center', va='center', alpha=0.5)

    shuffle(chords)
    chords = chords[:num_chords]
    i = 0

    def on_key(event):
        nonlocal i, samples
        if event.key == ' ':
            i += 1
            for j in range(sample_size):
                ax[j].cla()
            render(chords, sample_size, i, samples, fig, ax, counter)
            plt.draw()

    fig.canvas.mpl_connect('key_press_event', on_key)

    render(chords, sample_size, i, samples, fig, ax, counter)
    fig.subplots_adjust(left=0, right=1, hspace=0, wspace=0)
    plt.show()


def render(chords, sample_size, i, samples, fig, ax, counter):
    """Renders the i-th sample of chords, each onto a separate subplot in ax."""
    sampled_chords = chords[i * sample_size : (i + 1) * sample_size]
    if len(sampled_chords) < sample_size:
        plt.close(fig)

    for j, chord in enumerate(sampled_chords):
        chord_diagram(chord, ax[j], show_fingering=True)
    counter.set_text(f'{i + 1}/{samples}')


def parse_tag(tag) -> list[Chord]:
    """Parses a tag file or a comma-separated list into a list of chords."""
    chords = []
    if tag.endswith('.csv'):
        chords = load_chords(tag)
    else:
        for tag_chord in tag.split(','):
            name = tag_chord
            diagram = ''
            if '(' in tag_chord and tag_chord.endswith(')'):
                name, diagram = tag_chord.split('(')
                diagram = diagram[:-1]
            chords.append(Chord(name, diagram))

    return chords


def filter_chords(chords: list[Chord], include: list[Chord], exclude: list[Chord]):
    """Removes or keeps chords based on the include and exclude lists. Chords
    in the filter lists are matched by name, and if the diagram is specified,
    it must match as well."""
    if include:
        chords = [c for c in chords if c in include]
    elif exclude:
        chords = [c for c in chords if c not in exclude]
    return chords


if __name__ == '__main__':
    main()
