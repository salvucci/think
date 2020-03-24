import math

from think import Location, Module

from .hands import Hands


class Mousing(Module):

    def __init__(self, agent, mouse, vision, hands=None):
        super().__init__("mousing", agent)
        self.mouse = mouse
        self.vision = vision
        self.hands = hands or Hands(agent)
        self.worker = hands.worker
        self.loc = Location(0, 0)
        self.init_time = .050
        self.burst_time = .050
        self.fitts_coeff = .100
        self.min_fitts_time = .100

    def fitts(self, coeff, d, w):
        if w <= 0:
            w = 1  # vis.Vision.pixel_to_degree(1.0)
        f = math.log((d / w) + .5) / math.log(2)
        return max(self.min_fitts_time, coeff * f)

    # this is only movement, what about all time?
    def movement_time(self, from_loc, to_area):
        d = self.vision.display.pixels_to_inches(from_loc.distance_to(to_area))
        w = self.vision.display.pixels_to_inches(
            to_area.approach_width_from(from_loc))
        return self.init_time + max(self.burst_time, self.fitts(self.fitts_coeff, d, w))

    def calc_move_time(self, loc1, loc2):
        d = self.vision.display.pixels_to_degrees(loc1.distance_to(loc2))
        w = self.vision.display.pixels_to_degrees(
            loc2.approach_width_from(loc1))
        return self.init_time + max(self.burst_time, self.fitts(self.fitts_coeff, d, w))

    def start_move_to(self, visual):
        self.worker.acquire()
        self.think("move mouse {}".format(visual))
        self.log("moving mouse {}".format(visual))
        self.vision.start_encode(visual)
        duration = self.calc_move_time(self.loc, visual)

        def fn():
            self.loc = visual
            self.mouse.move(visual.x, visual.y)

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
                        self.mouse.click()

        self.worker.run(duration, "click mouse {}".format(self.loc), fn)

    def click(self):
        self.start_click()
        self.worker.wait_until_free()

    def point_and_click(self, visual):
        self.move_to(visual)
        self.vision.get_encoded()
        self.click()
