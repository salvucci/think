import math
import re
from think import Module, Worker, Location


class Hands(Module):
    ON_KEYBOARD = 1
    ON_MOUSE = 2

    def __init__(self, agent, pos=None):
        super().__init__("hands", agent)
        self.pos = pos if pos is not None else Hands.ON_KEYBOARD
        self.worker = Worker("hands", self)

    def on_mouse(self):
        return self.pos == Hands.ON_MOUSE

    def on_keyboard(self):
        return self.pos == Hands.ON_KEYBOARD

    def move(self, pos):
        self.pos = pos
        return self


class Keyboard:
    KEY_TUPLES = [('a', False, "a"), ('b', False, "b"),
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
        for t in Keyboard.KEY_TUPLES:
            self._char_to_code[t[0]] = t[2]
            self._char_to_shifted[t[0]] = t[1]
            self._code_to_char[t[2]] = t[0]

    def code(self, c):
        return self._char_to_code[c]

    def shifted(self, c):
        return self._char_to_shifted[c]

    def char(self, code):
        return self._code_to_char[code]


class Typing(Module):
    DEFAULT_WPM = 40

    def __init__(self, hands, keyboard=Keyboard()):
        super().__init__("hands", hands.agent)
        self.hands = hands
        self.keyboard = keyboard
        self.worker = hands.worker
        self.type_fns = []
        self.wpm(Typing.DEFAULT_WPM)

    def add_type_fn(self, fn):
        self.type_fns.append(fn)
        return self

    def key_time(self, wpm):
        return .0000083 * (wpm * wpm) - .003051 * wpm + .31727

    def wpm(self, wpm=None):
        if wpm:
            self._wpm = wpm
            self._key_time = self.key_time(wpm)
        return self._wpm

    def keys(self, burst):
        keys = []
        shifted = False
        for c in burst:
            if (self.keyboard.shifted(c) is not shifted):
                shifted = not shifted
                keys.append('shift')
            keys.append(c)
        if shifted:
            keys.append('shift')
        return keys

    def bursts(self, text):
        text = str(text)
        pattern = re.compile(r'([A-Za-z]+|[^A-Za-z])')
        return re.findall(pattern, text)

    def typing_time(self, text, wpm=DEFAULT_WPM):
        time = 0
        key_time = self.key_time(wpm)
        for burst in self.bursts(text):
            time += .050 + key_time * len(self.keys(burst))
        return time

    def type(self, text):
        for burst in self.bursts(text):
            self.worker.acquire()
            self.think("type \"{}\"".format(burst))
            self.log("typing \"{}\"".format(burst))

            def fn():
                shifted = False
                for key in self.keys(burst):
                    self.wait(self._key_time)
                    if key is "shift":
                        shifted = not shifted
                        self.log("{} '{}'".format(
                            "pressed" if shifted else "released", key))
                    else:
                        self.log("typed '{}'".format(key))
                    for fn in self.type_fns:
                        fn(key)
            self.worker.run(action=fn)


class Mouse(Module):

    def __init__(self, hands, vision):
        super().__init__("hands", hands.agent)
        self.hands = hands
        self.vision = vision
        self.worker = hands.worker
        self.loc = Location(0, 0)
        self.move_fns = []
        self.click_fns = []
        self.init_time = .050
        self.burst_time = .050
        self.fitts_coeff = .100
        self.min_fitts_time = .100

    def add_move_fn(self, fn):
        self.move_fns.append(fn)
        return self

    def add_click_fn(self, fn):
        self.click_fns.append(fn)
        return self

    def fitts(self, coeff, d, w):
        if w <= 0:
            w = 1  # vis.Vision.pixel_to_degree(1.0)
        f = math.log((d / w) + .5) / math.log(2)
        return max(self.min_fitts_time, coeff * f)

    # this is only movement, what about all time?
    def movement_time(self, from_loc, to_area):
        d = self.vision.display.pixels_to_inches(from_loc.distance_to(to_area))
        w = self.vision.display.pixels_to_inches(to_area.approach_width_from(from_loc))
        return self.init_time + max(self.burst_time, self.fitts(self.fitts_coeff, d, w))

    def calc_move_time(self, loc1, loc2):
        d = self.vision.display.pixels_to_degrees(loc1.distance_to(loc2))
        w = self.vision.display.pixels_to_degrees(loc2.approach_width_from(loc1))
        return self.init_time + max(self.burst_time, self.fitts(self.fitts_coeff, d, w))

    def start_move_to(self, visual):
        self.worker.acquire()
        self.think("move mouse {}".format(visual))
        self.log("moving mouse {}".format(visual))
        self.vision.start_encode(visual)
        duration = self.calc_move_time(self.loc, visual)

        def fn():
            self.loc = visual
            for fn in self.move_fns:
                fn(visual)
        self.worker.run(duration, "moved mouse {}".format(visual), fn)

    def move_to(self, visual):
        self.start_move_to(visual)
        self.worker.wait_until_free()
        return self

    def calc_click_time(self):
        return self.init_time + 2 * self.burst_time

    def start_click(self):
        self.worker.acquire()
        self.think("click mouse")
        self.log("clicking mouse")
        duration = self.calc_click_time()

        def fn():
            if self.loc is not None:
                for visual in self.vision.visuals:
                    if visual.contains(self.loc):
                        for fn in self.click_fns:
                            fn(visual)
        self.worker.run(duration, "click mouse {}".format(self.loc), fn)

    def click(self):
        self.start_click()
        self.worker.wait_until_free()

    def point_and_click(self, visual):
        self.move_to(visual)
        self.vision.get_encoded()
        self.click()
