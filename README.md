# 🎵 Music Theory Anki Cards

This repository contains scripts for generating Anki cards suitable for
practicing different music theory concepts. All the cards are generated
programmatically, for all different keys. The required images are either
fetched from the web or generated as needed using Matplotlib.

## Decks

- [Circle of Fifths](anki/decks/circle_of_fifths.py):
  - relative major/minor keys,
  - number of accidentals,
  - key signatures,
  - accidentals in each key,
  - perfect fourths and fifths between keys.

- [Guitar Chord Notes](anki/decks/guitar_chord_notes.py):
  - guitar chord names,
  - note names in each chord,
  - scale degrees in each chord.

## Practice scripts

The repository also contains scripts that can be used for different practices.

- [Shuffled Notes](practices/shuffled_notes.py): Generate a set of randomly
shuffled notes. It can be used for practicing notes on the guitar neck:
generate a set of notes, each note is played on each string, changing the
note when reaching the E/e string.
