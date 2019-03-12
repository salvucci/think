import re
from think import Module
from .machine import Keyboard


class Typing(Module):
    DEFAULT_WPM = 40

    def __init__(self, hands, keyboard=Keyboard()):
        super().__init__("typing", hands.agent)
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
