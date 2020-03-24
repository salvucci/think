import math
import random

from think import Location, Module


class Eyes(Module):

    def __init__(self, agent):
        super().__init__("eyes", agent)
        self.vision = None
        self.loc = Location(0, 0)
        self.last_prep_cancel = None
        self.fixate_fns = []
        self.enc_time_f = .001
        self.enc_time_exp = .4
        self.prep_time = .150
        self.exec_time_base = .070
        self.exec_time_inc = .002

    def set_vision(self, vision):
        self.vision = vision

    def add_fixate_fn(self, fn):
        self.fixate_fns.append(fn)

    def move_to(self, x, y):
        self.loc = Location(x, y)

    def _compute_eccentricity(self, visual):
        return self.vision.display.pixels_to_degrees(self.loc.distance_to(visual))

    def compute_enc_time(self, visual):
        freq = visual.freq
        if freq is not None:
            return (self.enc_time_f * -math.log(freq)
                    * math.exp(self.enc_time_exp * self._compute_eccentricity(visual)))
        else:
            return self.vision.default_enc_time

    def _rand_time(self, time):
        return max(time + random.gauss(0, time / 3), .001)

    def prepare(self, visual, obj, enc_start, enc_dur):
        if self.last_prep_cancel is not None:
            self.last_prep_cancel.try_cancel()
        sd = .1 * \
            self.vision.display.degrees_to_pixels(
                self._compute_eccentricity(visual))
        new_loc = Location(visual.x + random.gauss(0, sd),
                           visual.y + random.gauss(0, sd))
        self.log("prepare {}".format(new_loc))
        duration = self._rand_time(self.prep_time)

        def fn():
            self.move(visual, obj, new_loc, enc_start, enc_dur)

        self.last_prep_cancel = self.run_thread_can_cancel(fn, duration)

    def move(self, visual, obj, new_loc, enc_start, enc_dur):
        self.log("move {}".format(new_loc))
        duration = self._rand_time(
            self.exec_time_base) + self.exec_time_inc * self._compute_eccentricity(visual)

        def fn():
            self.log("moved {}".format(new_loc))
            self.loc = new_loc
            if enc_start + enc_dur > self.time():
                completed = (self.time() - enc_start) / enc_dur
                new_time = self.compute_enc_time(visual)
                rem_dur = (1 - completed) * new_time
                if rem_dur > 0:
                    self.vision.start_encode_thread(visual, obj, rem_dur)
                    self.prepare(visual, obj, self.time(), rem_dur)
            for fn in self.fixate_fns:
                fn(self.loc)

        self.run_thread(fn, duration)
