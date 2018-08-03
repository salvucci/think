import math


class Display:

    def __init__(self, viewing_distance=30, pixels_per_inch=72):
        self.viewing_distance = viewing_distance
        self.pixels_per_inch = pixels_per_inch

    def pixels_to_inches(self, pixels):
        return pixels / self.pixels_per_inch

    def pixels_to_degrees(self, pixels):
        return math.degrees(math.atan2(pixels / self.pixels_per_inch, self.viewing_distance))

    def degrees_to_pixels(self, angle):
        return self.viewing_distance * math.tan(math.radians(angle)) * self.pixels_per_inch


class Keyboard:

    _KEY_TUPLES = [('a', False, "a"), ('b', False, "b"),
                  ('c', False, "c"), ('d', False, "d"), ('e', False, "e"),
                  ('f', False, "f"), ('g', False, "g"), ('h', False, "h"),
                  ('i', False, "i"), ('j', False, "j"), ('k', False, "k"),
                  ('l', False, "l"), ('m', False, "m"), ('n', False, "n"),
                  ('o', False, "o"), ('p', False, "p"), ('q', False, "q"),
                  ('r', False, "r"), ('s', False, "s"), ('t', False, "t"),
                  ('u', False, "u"), ('v', False, "v"), ('w', False, "w"),
                  ('x', False, "x"), ('y', False, "y"), ('z', False, "z"),
                  ('A', True, "A"), ('B', True, "B"), ('C', True, "C"),
                  ('D', True, "D"), ('E', True, "E"), ('F', True, "F"),
                  ('G', True, "G"), ('H', True, "H"), ('I', True, "I"),
                  ('J', True, "J"), ('K', True, "K"), ('L', True, "L"),
                  ('M', True, "M"), ('N', True, "N"), ('O', True, "O"),
                  ('P', True, "P"), ('Q', True, "Q"), ('R', True, "R"),
                  ('S', True, "S"), ('T', True, "T"), ('U', True, "U"),
                  ('V', True, "V"), ('W', True, "W"), ('X', True, "X"),
                  ('Y', True, "Y"), ('Z', True, "Z"),
                  ('`', False, "back_quote"), ('~', True, "back_quote"),
                  ('0', False, "0"), ('1', False, "1"), ('2', False, "2"),
                  ('3', False, "3"), ('4', False, "4"), ('5', False, "5"),
                  ('6', False, "6"), ('7', False, "7"), ('8', False, "8"),
                  ('9', False, "9"), ('-', False, "minus"),
                  ('=', False, "equals"),
                  ('!', True, "exclamation_mark"), ('@', True, "at"),
                  ('#', True, "number_sign"), ('$', True, "dollar"),
                  ('%', True, "5"), ('^', True, "circumflex"),
                  ('&', True, "ampersand"), ('*', True, "asterisk"),
                  ('(', True, "left_parenthesis"),
                  (')', True, "right_parenthesis"),
                  ('_', True, "underscore"), ('+', True, "plus"),
                  ('\t', False, "tab"), ('\n', False, "enter"),
                  ('[', False, "open_bracket"),
                  (']', False, "close_bracket"),
                  ('\\', False, "back_slash"),
                  ('{', True, "open_bracket"),
                  ('}', True, "close_bracket"),
                  ('|', True, "back_slash"), (';', False, "semicolon"),
                  ('\'', False, "quote"), (':', True, "colon"),
                  ('"', True, "quotedbl"), (',', False, "comma"),
                  ('.', False, "period"), ('/', False, "slash"),
                  ('<', True, "comma"), ('>', True, "period"),
                  ('?', True, "slash"), (' ', False, "space"),
                  (None, False, "shift")]

    def __init__(self):
        self._char_to_code = {}
        self._char_to_shifted = {}
        self._code_to_char = {}
        for t in Keyboard._KEY_TUPLES:
            self._char_to_code[t[0]] = t[2]
            self._char_to_shifted[t[0]] = t[1]
            self._code_to_char[t[2]] = t[0]

    def code(self, c):
        return self._char_to_code[c]

    def shifted(self, c):
        return self._char_to_shifted[c]

    def char(self, code):
        return self._code_to_char[code]
