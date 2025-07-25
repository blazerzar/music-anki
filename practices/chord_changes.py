"""A Python script for sampling random chords for practicing changing between
them.

Usage:
    python practices/chord_changes.py [ukulele|chords csv file path] [options]

Examples:
    python practices/chord_changes.py --n 3
    python practices/chord_changes.py ukulele
    python practices/chord_changes.py my_chords.csv --chords 10 --n 4

Arguments:
    --chords num: number of chord samples, by default, all chords are used
    --n num: chord sample size, default is 2
    --help: show script usage documentation

Pressing space will show the next sample of chords, and q will quit the program.
"""

import sys
from os import path
from random import shuffle

import matplotlib.pyplot as plt

sys.path.append(path.join(path.dirname(path.abspath(__file__)), '..'))
from utils import chord_diagram, load_chords

GUITAR_CHORDS = path.join('data', 'guitar_chords.csv')
UKULELE_CHORDS = path.join('data', 'ukulele_chords.csv')


def main():
    chords_file = GUITAR_CHORDS
    num_chords = None
    sample_size = 2

    for i, arg in enumerate(sys.argv):
        if arg == '--chords' and i + 1 < len(sys.argv):
            num_chords = int(sys.argv[i + 1])
        elif arg == '--n' and i + 1 < len(sys.argv):
            sample_size = int(sys.argv[i + 1])
        elif arg == '--help':
            print(__doc__, end='')
            exit(0)
        elif i == 1 and arg == 'ukulele':
            chords_file = UKULELE_CHORDS
        elif i == 1 and arg.endswith('.csv'):
            chords_file = arg

    chords = load_chords(chords_file)
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


if __name__ == '__main__':
    main()
