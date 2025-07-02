import genanki

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
