# 🎵 Music Theory Anki Cards

This repository contains scripts for generating Anki cards suitable for
practicing different music theory concepts. All the cards are generated
programmatically, for all different keys. The required images are either
fetched from the web or generated as needed using Matplotlib.

## Decks

- [Circle of Fifths](decks/circle_of_fifths.py):
  - relative major/minor keys,
  - number of accidentals,
  - key signatures,
  - accidentals in each key,
  - perfect fourths and fifths between keys.

- [Guitar Chord Notes](decks/guitar_chord_notes.py):
  - guitar chord names,
  - note names in each chord,
  - scale degrees in each chord.

- [Note Distances](decks/note_distances.py): size of intervals between notes.

- [Interval Sizes](decks/interval_sizes.py): size of named intervals.

## Practice scripts

The repository also contains scripts that can be used for different practices.

- [Shuffled Notes](practices/shuffled_notes.py): Generate a set of randomly
shuffled notes. It can be used for practicing notes on the guitar neck:
generate a set of notes, each note is played on each string, changing the
note when reaching the E/e string.

<p align="center">
  <img src="screenshots/shuffled_notes.png" alt="Shuffled Notes" width="300px">
</p>

- [Chord Changes](practices/chord_changes.py): Generate samples of chords to
practice chord changes between them.

<p align="center">
  <img src="screenshots/chord_changes_guitar.png" alt="Chord Changes" height="300px">
  <img src="screenshots/chord_changes_ukulele.png" alt="Chord Changes" height="300px">
</p>
