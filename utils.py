import genanki
import matplotlib.pyplot as plt

styling = """
.card {
    font-family: arial;
    font-size: 20px;
    text-align: center;
    color: black;
    background-color: white;
}

.card .back {
    text-align: left;
}
"""

card_model = genanki.Model(
    1464519481,
    'Basic Music Card',
    fields=[
        {'name': 'Front', 'font': 'Arial'},
        {'name': 'Back', 'font': 'Arial'},
    ],
    templates=[
        {
            'name': 'Card 1',
            'qfmt': '{{Front}}',
            'afmt': '{{FrontSide}}<hr id="answer">{{Back}}',
        },
    ],
    css=styling,
)


def note_to_latex(note):
    name = r'\text{' + note[0] + '}'
    for accidental in note[1:]:
        if accidental == '#':
            name += r'\sharp'
        elif accidental == 'b':
            name += r'\flat'
    return r'\(' + name + r'\)'


def degree_to_latex(degree):
    name = ''
    for c in degree:
        if c == '#':
            name += r'\sharp'
        elif c == 'b':
            name += r'\flat'
        elif c.isdigit():
            name += c
    return r'\(' + name + r'\)'


def chord_to_latex(chord):
    name = ''
    i = 0
    while i < len(chord):
        if chord[i] not in ['#', 'b', '/'] and not chord[i].isdigit():
            name += r'\text{' + chord[i]
            i += 1
            while (
                i < len(chord)
                and chord[i].isalpha()
                and chord[i] not in ['#', 'b', '/']
            ):
                name += chord[i]
                i += 1
            name += '}'
            continue
        elif chord[i] == '#':
            name += r'\sharp'
        elif chord[i] == 'b':
            name += r'\flat'
        else:
            name += chord[i]
        i += 1
    return r'\(' + name + r'\)'


class Chord:
    def __init__(self, name, diagram, fingering, notes, degrees):
        """Initializes a chord with its name, diagram, fingering, notes, and
        degrees. The diagram, fingering, notes and degrees are space-separated
        strings, with unused strings represented by 'x' in all cases.
        """
        self.name = name
        self.diagram = [None if d == 'x' else int(d) for d in diagram.split()]
        self.fingering = [None if f == 'x' else int(f) for f in fingering.split()]
        self.notes = notes.split()
        self.degrees = degrees.split()

        d = len(self.diagram)
        f = len(self.fingering)
        n = len(self.notes)
        deg = len(self.degrees)
        assert len({d, f, n, deg}) == 1

    def __repr__(self):
        return f'{self.name}({self.diagram}, {self.fingering})'


def load_chords(filename) -> list[Chord]:
    chords = []
    with open(filename, 'r', encoding='utf-8') as f:
        next(f)
        for line in f:
            args = line.strip().split(',')
            chords.append(Chord(*args))
    return chords


def blank_diagram(ax, num_strings, first_fret=1):
    """Draws a blank chord diagram on the given axes. Number of strings is
    supplied to support guitar and ukulele chords. If the first fret is 1,
    the nut is drawn, otherwise we instead write the fret number."""
    if num_strings < 2:
        raise ValueError('Number of strings must be at least 2.')

    # Frame
    w, h = num_strings - 1, 7
    ax.add_patch(plt.Rectangle((0, 0), w, h, ec='black', fc='white', lw=1.5))

    # Interior strings
    for x in range(num_strings - 2):
        ax.add_line(plt.Line2D([x + 1, x + 1], [0, h], color='black', lw=1.5))

    # Frets
    fret_length = num_strings - 1
    num_frets = 5
    for i in range(4):
        y = h * (i + 1) / num_frets
        ax.add_line(plt.Line2D([0, fret_length], [y, y], color='black', lw=1.5))

    if first_fret == 1:
        # Nut
        ax.add_patch(plt.Rectangle((0, h), fret_length, 0.1, color='black', lw=1.5))
    else:
        kwargs = {'fontsize': 16, 'ha': 'center', 'va': 'center'}
        x, y = fret_length + 0.55, (h + 0.7) - h / num_frets
        ax.text(x, y, str(first_fret), **kwargs)


def chord_diagram(chord: Chord, ax, show_fingering=False, show_name=True):
    if show_name:
        ax.set_title(chord.name, fontsize=32)

    num_strings = len(chord.diagram)
    lowest_fret = min(f for f in chord.diagram if f is not None)
    highest_fret = max(f for f in chord.diagram if f is not None)
    first_fret = 1 if highest_fret <= 5 else lowest_fret
    blank_diagram(ax, num_strings, first_fret)

    # Find and draw bars
    bars = {}
    for finger in [1, 2, 3, 4]:
        strings = [i for i, f in enumerate(chord.fingering) if f == finger]
        if len(strings) > 1:
            bar_start = min(strings)
            bar_end = max(strings)
            bars[finger] = bar_start, bar_end

            bar_fret = chord.diagram[bar_start] - first_fret + 1
            x, y = bar_start, 7.7 - 7 * bar_fret / 5 - 0.35
            width, height = bar_end - bar_start, 0.7
            ax.add_patch(plt.Rectangle((x, y), width, height, color='k', lw=0))

    for string, (fret, finger) in enumerate(zip(chord.diagram, chord.fingering)):
        if not fret:
            args = string, 7.5, 160
            m = 'x' if fret is None else 'o'
            kwargs = (
                {'c': 'black'}
                if fret is None
                else {'edgecolor': 'black', 'facecolor': 'white'}
            )
            ax.scatter(*args, marker=m, **kwargs, lw=2.2)
        else:
            y = 7.7 - 7 * (fret - first_fret + 1) / 5
            x = string
            if finger not in bars or string in bars[finger]:
                ax.add_patch(plt.Circle((x, y), 0.35, color='black', lw=0))
            if show_fingering:
                kwargs = {'ha': 'center', 'va': 'center', 'color': 'white'}
                ax.text(x, y - 0.05, finger, fontsize=14, **kwargs)

    ax.set_aspect('equal', adjustable='box')
    ax.set_xlim(-1, num_strings)
    ax.set_ylim(-0.1, 8)
    ax.axis('off')
