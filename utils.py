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
