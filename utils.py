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


def chord_diagram(
    diagram,
    fingering,
    name,
    show_fingering=False,
    show_name=True,
    fig=None,
    ax=None,
):
    if fig is None or ax is None:
        fig, ax = plt.subplots(figsize=(4, 6))
    if show_name:
        ax.set_title(name, fontsize=32)

    ax.add_patch(plt.Rectangle((0, 0), 5, 7, ec='black', fc='white', lw=1.5))
    # Strings
    for x in range(4):
        ax.add_line(plt.Line2D([x + 1, x + 1], [0, 7], color='black', lw=1.5))
    # Frets
    for i in range(4):
        y = 7 * (i + 1) / 5
        ax.add_line(plt.Line2D([0, 5], [y, y], color='black', lw=1.5))
    # Nut
    ax.add_patch(plt.Rectangle((0, 7), 5, 0.1, color='black', lw=1.5))

    # Find and draw bars
    bars = {}
    for finger in ['1', '2', '3', '4']:
        strings = [i for i, f in enumerate(fingering) if f == finger]
        if len(strings) > 1:
            bar_start = min(strings)
            bar_end = max(strings)
            bars[finger] = bar_start, bar_end

            bar_fret = int(diagram[bar_start])
            x, y = bar_start, 7.7 - 7 * bar_fret / 5 - 0.35
            width, height = bar_end - bar_start, 0.7
            ax.add_patch(plt.Rectangle((x, y), width, height, color='k', lw=0))

    for string, (fret, finger) in enumerate(zip(diagram, fingering)):
        if fret == 'x' or fret == '0':
            args = string, 7.5, 160
            m = 'x' if fret == 'x' else 'o'
            kwargs = (
                {'c': 'black'}
                if fret == 'x'
                else {'edgecolor': 'black', 'facecolor': 'white'}
            )
            ax.scatter(*args, marker=m, **kwargs, lw=2.2)
        else:
            fret = int(fret)
            y = 7.7 - 7 * fret / 5
            x = string
            if finger not in bars or string in bars[finger]:
                ax.add_patch(plt.Circle((x, y), 0.35, color='black', lw=0))
            if show_fingering:
                ax.text(
                    x,
                    y - 0.05,
                    finger,
                    fontsize=14,
                    ha='center',
                    va='center',
                    color='white',
                )

    ax.set_aspect('equal', adjustable='box')
    ax.axis('off')
    return fig, ax
