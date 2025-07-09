"""
Create an Anki deck for learning the circle of fifths:
    - Relative minors of major keys.
    - Relative majors of minor keys.
    - Number of sharps/flats in different keys.
    - Reading key signatures.
    - Perfect 4ths and 5ths between keys.
    - Accidentals in each key.
"""

import shutil
import urllib.request
from os import environ, mkdir, path, remove, rmdir

import genanki
from bs4 import BeautifulSoup

from utils import card_model, note_to_latex

EMAIL = environ.get('ANKI_BOT_EMAIL', '').strip()
USER_AGENT = f'MusicAnkiBot/1.0 ({EMAIL})'
TEMP_DIR = 'temp_circle_of_fifths'
OUTPUT_DIR = 'out'


def main():
    if not EMAIL:
        print('Email must be set to enable remote downloads.')
        exit(1)
    if not path.exists(OUTPUT_DIR):
        mkdir(OUTPUT_DIR)
    if not path.exists(TEMP_DIR):
        mkdir(TEMP_DIR)

    majors = 'C G D A E B F# C# Cb Gb Db Ab Eb Bb F'.split()
    minors = 'a e b f# c# g# d# a# ab eb bb f c g d'.split()
    accidentals = '0_ 1# 2# 3# 4# 5# 6# 7# 7b 6b 5b 4b 3b 2b 1b'.split()
    accidental_notes = 'F C G D A E B'.split()

    media_files = []
    deck = genanki.Deck(1831548167, 'Music::Circle of Fifths')

    for i, (maj, min, acc) in enumerate(zip(majors, minors, accidentals)):
        maj_tex = note_to_latex(maj)
        min_tex = note_to_latex(min)

        # What is the relative minor of the major key?
        note = genanki.Note(
            model=card_model,
            fields=[f'Relative minor of {maj_tex}', min_tex],
        )
        deck.add_note(note)

        # What is the relative major of the minor key?
        note = genanki.Note(
            model=card_model,
            fields=[f'Relative major of {min_tex}', maj_tex],
        )
        deck.add_note(note)

        # What is the number of sharps/flats in the key?
        sharps = int(acc[0]) if acc[1] == '#' else 0
        flats = int(acc[0]) if acc[1] == 'b' else 0
        answer = 'no accidentals'
        if sharps:
            answer = f'{sharps} sharp' + ('' if sharps == 1 else 's')
        elif flats:
            answer = f'{flats} flat' + ('' if flats == 1 else 's')
        note = genanki.Note(
            model=card_model,
            fields=[f'How many sharps/flats in {maj_tex}?', answer],
        )
        deck.add_note(note)
        note = genanki.Note(
            model=card_model,
            fields=[f'How many sharps/flats in {min_tex}?', answer],
        )
        deck.add_note(note)

        # Reading key signatures
        filename = download_key_signature(maj)
        media_files.append(path.join(TEMP_DIR, filename))
        note = genanki.Note(
            model=card_model,
            fields=[
                f'<img class="key-img" src="{filename}" width="200px">',
                f'{maj_tex} / {min_tex}',
            ],
        )
        deck.add_note(note)

        # Accidentals in each key
        acc_notes = []
        if sharps:
            acc_notes = [f'{n}#' for n in accidental_notes[:sharps]]
        elif flats:
            acc_notes = [f'{n}b' for n in accidental_notes[: -(flats + 1) : -1]]
        for key in [maj_tex, min_tex]:
            note = genanki.Note(
                model=card_model,
                fields=[
                    f'What are the accidentals in {key}?',
                    ' '.join(note_to_latex(n) for n in acc_notes) or '-',
                ],
            )
            deck.add_note(note)

        if maj == 'C#' or maj == 'Cb':
            continue

        # Neighboring keys
        fourth = majors[(i - 1) % len(majors)]
        fifth = majors[(i + 1) % len(majors)]
        note = genanki.Note(
            model=card_model,
            fields=[
                f'What are the P4 and P5 of {maj_tex}?',
                f'{note_to_latex(fourth)} and {note_to_latex(fifth)}',
            ],
        )
        deck.add_note(note)

    package = genanki.Package(deck)
    package.media_files = media_files
    package.write_to_file(f'{OUTPUT_DIR}/circle_of_fifths.apkg')

    for filename in media_files:
        remove(filename)
    rmdir(TEMP_DIR)


def note_to_filename(note):
    """Convert key signature into a filename for key signature images."""
    # Currently, the C# key file is named differently
    if note == 'C#':
        return 'Key_Signature_of_C-sharp_major.jpg'

    quality = 'major' if note[0].isupper() else 'minor'
    key = note[0].upper()
    if len(note) == 2:
        key += '-sharp' if note[1] == '#' else '-flat'
    filename = f'Key_Signature_{key}_{quality}.jpg'
    return filename


def download_key_signature(note):
    # Download Wikipedia web page to find the image URL
    filename = note_to_filename(note)
    url = 'https://en.wikipedia.org/wiki/File:' + filename
    req = urllib.request.Request(url, headers={'User-Agent': USER_AGENT})
    html = urllib.request.urlopen(req).read()
    soup = BeautifulSoup(html, 'html.parser')

    img_element = soup.select_one(f'img[src$="{filename}"]')
    if img_element is None:
        raise ValueError(f'Image for {note} not found on Wikipedia.')
    img_url = 'https:' + img_element['src']
    req = urllib.request.Request(img_url, headers={'User-Agent': USER_AGENT})
    with (
        urllib.request.urlopen(req) as response,
        open(path.join(TEMP_DIR, filename), 'wb') as out_file,
    ):
        shutil.copyfileobj(response, out_file)

    return filename


if __name__ == '__main__':
    main()
