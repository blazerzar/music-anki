"""A Python script for sampling random chords for practicing changing between
them.

Usage:
    python practices/chord_changes.py [options]

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
from utils import chord_diagram

CHORDS_FILE = path.join('data', 'chords.csv')


def main():
    chords = load_chords(CHORDS_FILE)
    num_chords = len(chords)
    sample_size = 2

    for i, arg in enumerate(sys.argv):
        if arg == '--chords' and i + 1 < len(sys.argv):
            num_chords = int(sys.argv[i + 1])
        elif arg == '--n' and i + 1 < len(sys.argv):
            sample_size = int(sys.argv[i + 1])
        elif arg == '--help':
            print(__doc__, end='')
            exit(0)

    plt.rcParams['toolbar'] = 'None'
    fig, ax = plt.subplots(1, sample_size, figsize=(3.3 * sample_size, 5.5))
    fig.canvas.manager.set_window_title('Chord Changes')
    if sample_size == 1:
        ax = [ax]

    shuffle(chords)
    chords = chords[:num_chords]
    i = 0

    def on_key(event):
        nonlocal i
        if event.key == ' ':
            i += sample_size
            for j in range(sample_size):
                ax[j].cla()
            render(chords, sample_size, i, fig, ax)
            plt.draw()

    fig.canvas.mpl_connect('key_press_event', on_key)

    render(chords, sample_size, i, fig, ax)
    fig.subplots_adjust(left=0, right=1, hspace=0, wspace=0)
    plt.show()


def load_chords(filename):
    chords = []
    with open(filename, 'r', encoding='utf-8') as f:
        next(f)
        for line in f:
            name, diagram, fingering, notes, degrees = line.strip().split(',')
            chords.append((name, diagram, fingering, notes, degrees))
    return chords


def render(chords, sample_size, i, fig, ax):
    """Renders the i-th sample of chords, each onto a separate subplot in ax."""
    sampled_chords = chords[i : i + sample_size]
    if len(sampled_chords) < sample_size:
        plt.close(fig)

    for j, (name, diagram, fingering, *_) in enumerate(sampled_chords):
        chord_diagram(
            diagram,
            fingering,
            name,
            fig=fig,
            ax=ax[j],
            show_fingering=True,
        )
        ax[j].set_ylim(-0.1, 8.5)
        ax[j].set_xlim(-1, 6)


if __name__ == '__main__':
    main()
