import math
import re

from think import Location, Module, Worker


class Hands(Module):
    ON_KEYBOARD = 1
    ON_MOUSE = 2
    DEFAULT_TYPING_WPM = 40

    def __init__(self, agent, vision, machine, pos=None):
        super().__init__('hands', agent)
        self.vision = vision
        self.display = machine.display
        self.keyboard = machine.keyboard
        self.mouse = machine.mouse
        self.pos = pos or Hands.ON_KEYBOARD
        self.worker = Worker('hands', self)
        self.wpm(Hands.DEFAULT_TYPING_WPM)
        self.mouse_loc = Location(0, 0)
        self.mouse_init_time = .050
        self.mouse_burst_time = .050
        self.mouse_fitts_coeff = .100
        self.mouse_min_fitts_time = .100

    def on_mouse(self):
        return self.pos == Hands.ON_MOUSE

    def on_keyboard(self):
        return self.pos == Hands.ON_KEYBOARD

    def move(self, pos):
        self.pos = pos
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

    def typing_time(self, text, wpm=DEFAULT_TYPING_WPM):
        time = 0
        key_time = self.key_time(wpm)
        for burst in self.bursts(text):
            time += .050 + key_time * len(self.keys(burst))
        return time

    def type(self, text):
        for burst in self.bursts(text):
            self.worker.acquire()
            self.think('type "{}"'.format(burst))
            self.log('typing "{}"'.format(burst))

            def fn():
                shifted = False
                for key in self.keys(burst):
                    self.wait(self._key_time)
                    if key == 'shift':
                        shifted = not shifted
                        self.log('{} "{}"'.format(
                            'pressed' if shifted else 'released', key))
                    else:
                        self.log('typed "{}"'.format(key))
                    self.keyboard.type(key)
            self.worker.run(action=fn)

    def fitts(self, coeff, d, w):
        if w <= 0:
            w = 1  # vis.Vision.pixel_to_degree(1.0)
        f = math.log((d / w) + .5) / math.log(2)
        return max(self.mouse_min_fitts_time, coeff * f)

    # this is only movement, what about all time?
    def movement_time(self, from_loc, to_area):
        d = self.vision.display.pixels_to_inches(from_loc.distance_to(to_area))
        w = self.vision.display.pixels_to_inches(
            to_area.approach_width_from(from_loc))
        return self.mouse_init_time + max(self.mouse_burst_time, self.fitts(self.mouse_fitts_coeff, d, w))

    def calc_move_time(self, loc1, loc2):
        d = self.vision.display.pixels_to_degrees(loc1.distance_to(loc2))
        w = self.vision.display.pixels_to_degrees(
            loc2.approach_width_from(loc1))
        return self.mouse_init_time + max(self.mouse_burst_time, self.fitts(self.mouse_fitts_coeff, d, w))

    def start_move_to(self, visual):
        self.worker.acquire()
        self.think('move mouse {}'.format(visual))
        self.log('moving mouse {}'.format(visual))
        self.vision.start_encode(visual)
        duration = self.calc_move_time(self.mouse_loc, visual)

        def fn():
            self.mouse_loc = visual
            self.mouse.move(visual.x, visual.y)

        self.worker.run(duration, 'moved mouse {}'.format(visual), fn)

    def move_to(self, visual):
        self.start_move_to(visual)
        self.worker.wait_until_free()
        return self

    def calc_click_time(self):
        return self.mouse_init_time + 2 * self.mouse_burst_time

    def start_click(self):
        self.worker.acquire()
        self.think('click mouse')
        self.log('clicking mouse')
        duration = self.calc_click_time()

        def fn():
            if self.mouse_loc is not None:
                for visual in self.vision.visuals:
                    if visual.contains(self.mouse_loc):
                        self.mouse.click()

        self.worker.run(duration, 'click mouse {}'.format(self.mouse_loc), fn)

    def click(self):
        self.start_click()
        self.worker.wait_until_free()

    def point_and_click(self, visual):
        self.move_to(visual)
        self.vision.get_encoded()
        self.click()
