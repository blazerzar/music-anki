import unittest

from utils import chord_to_latex, degree_to_latex, note_to_latex


class TestConvToLatex(unittest.TestCase):
    def test_note_to_latex(self):
        for arg, out in [
            ('C', r'\(\text{C}\)'),
            ('C#', r'\(\text{C}\sharp\)'),
            ('Bb', r'\(\text{B}\flat\)'),
            ('fbb', r'\(\text{f}\flat\flat\)'),
            ('bbbb#', r'\(\text{b}\flat\flat\flat\sharp\)'),
            ('a#b#b', r'\(\text{a}\sharp\flat\sharp\flat\)'),
        ]:
            self.assertEqual(note_to_latex(arg), out)

    def test_degree_to_latex(self):
        for arg, out in [
            ('1', r'\(1\)'),
            ('#3', r'\(\sharp3\)'),
            ('b5', r'\(\flat5\)'),
            ('b13', r'\(\flat13\)'),
        ]:
            self.assertEqual(degree_to_latex(arg), out)

    def test_chord_to_latex(self):
        for arg, out in [
            ('C', r'\(\text{C}\)'),
            ('C#', r'\(\text{C}\sharp\)'),
            ('Bb', r'\(\text{B}\flat\)'),
            ('Cmaj7', r'\(\text{Cmaj}7\)'),
            ('C7#9', r'\(\text{C}7\sharp9\)'),
            ('Cm7b5', r'\(\text{Cm}7\flat5\)'),
            ('Dadd4', r'\(\text{Dadd}4\)'),
            ('F#m7b5', r'\(\text{F}\sharp\text{m}7\flat5\)'),
            ('D#sus2', r'\(\text{D}\sharp\text{sus}2\)'),
            ('Cbdim7', r'\(\text{C}\flat\text{dim}7\)'),
            ('A#/Dadd13', r'\(\text{A}\sharp/\text{Dadd}13\)'),
        ]:
            self.assertEqual(chord_to_latex(arg), out)


if __name__ == '__main__':
    unittest.main()
