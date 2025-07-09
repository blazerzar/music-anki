#!/bin/bash

. .venv/bin/activate
email=$(git config user.email)

for deck in decks/*.py; do
    echo "Running $(basename "$deck")"
    module=$(echo "$deck" | sed 's/\//./g' | sed 's/\.py$//')
    ANKI_BOT_EMAIL=$email python -m "$module"

    if [[ "$deck" == "decks/guitar_chord_notes.py" ]]; then
        echo "Running guitar_chord_notes.py for ukulele"
        python -m "$module" ukulele
    fi
done
