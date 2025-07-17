"""Creates a deck for learning the number of half steps in intervals."""

from os import path

import genanki

from utils import card_model

OUTPUT_DIR = 'out'


def main():
    intervals = {
        1: ('perfect', 0),
        2: ('major', 2),
        3: ('major', 4),
        4: ('perfect', 5),
        5: ('perfect', 7),
        6: ('major', 9),
        7: ('major', 11),
        8: ('perfect', 12),
    }

    # To create questions like "Which intervals are _ number of half steps?"
    inverse_lookup = {}

    deck = genanki.Deck(1664199498, 'Music::Interval Sizes')

    for interval, (quality, half_steps) in intervals.items():
        qualified_intervals = []

        if quality == 'perfect':
            qualified_intervals += [(f'P{interval}', half_steps)]
            qualified_intervals += [(f'A{interval}', half_steps + 1)]
            if half_steps >= 1:
                qualified_intervals += [(f'd{interval}', half_steps - 1)]
        elif quality == 'major':
            qualified_intervals += [(f'M{interval}', half_steps)]
            qualified_intervals += [(f'm{interval}', half_steps - 1)]
            qualified_intervals += [(f'A{interval}', half_steps + 1)]
            qualified_intervals += [(f'd{interval}', half_steps - 2)]
        else:
            raise ValueError(f'Unknown quality: {quality}')

        for name, size in qualified_intervals:
            inverse_lookup.setdefault(size, []).append(name)
            note = genanki.Note(
                model=card_model,
                fields=[f'How large is {name}?', f'{size} half steps'],
            )
            deck.add_note(note)

    for size, names in inverse_lookup.items():
        note = genanki.Note(
            model=card_model,
            fields=[f'Which intervals equal {size} half steps?', ', '.join(names)],
        )
        deck.add_note(note)

    package = genanki.Package(deck)
    package.write_to_file(path.join(OUTPUT_DIR, 'interval_sizes.apkg'))


if __name__ == '__main__':
    main()
