import math
import random
from think import Module, Buffer, Location, Area, Query


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


class Visual(Area):

    def __init__(self, x, y, w, h, isa):
        super().__init__(x, y, w, h, isa)
        self.set('seen', False)
        self.freq = None


class Vision(Module):

    def __init__(self, agent, eyes=None, display=Display()):
        super().__init__("vision", agent)
        self.display = display
        self.eyes = eyes
        if eyes is not None:
            eyes.set_vision(self)
        self.visuals = {}
        self.find_buffer = Buffer("vision.find", self)
        self.encode_buffer = Buffer("vision.encode", self)
        self.encode_loc = Location(0, 0)
        self.wait_for_query = None
        self.last_encode_cancel = None
        self.attend_fns = []
        self.encode_fns = []
        self.find_time = .000
        self.default_enc_time = .135

    def add(self, visual, obj):
        self.visuals[visual] = obj
        if self.wait_for_query is not None and self.wait_for_query.matches(visual):
            self._finish_wait_for(visual)
        return self

    def remove(self, visual):
        del self.visuals[visual]
        return self

    def clear(self):
        self.visuals = {}
        return self

    def add_attend_fn(self, fn):
        self.attend_fns.append(fn)
        return self

    def add_encode_fn(self, fn):
        self.encode_fns.append(fn)
        return self

    def _try_find(self, query):
        match = None
        match_dist = 0
        for visual in self.visuals.keys():
            if query is not None and query.matches(visual):
                current = self.eyes.loc if self.eyes is not None else self.encode_loc
                dist = current.distance_to(visual)
                if match is None or dist < match_dist:
                    match = visual
                    match_dist = dist
        return match

    def start_find(self, query=None, **kwargs):
        if not query:
            query = Query(**kwargs)
        self.find_buffer.acquire()
        self.think("find {}".format(query))
        match = self._try_find(query)
        duration = self.find_time
        if match is not None:
            def fn():
                for fn in self.attend_fns:
                    fn(match)
            self.find_buffer.set(match, duration, "found {}".format(match), fn)
        else:
            self.find_buffer.clear(duration, "find failed")

    def get_found(self):
        return self.find_buffer.get_and_release()

    def find(self, query=None, **kwargs):
        if not query:
            query = Query(**kwargs)
        self.start_find(query)
        return self.get_found()

    def start_wait_for(self, query=None, **kwargs):
        if not query:
            query = Query(**kwargs)
        self.find_buffer.acquire()
        self.think("wait for {}".format(query))
        visual = self._try_find(query.eq('seen', False))
        if visual is not None:
            self._finish_wait_for(visual)
        else:
            self.wait_for_query = query

    def _finish_wait_for(self, visual):
        self.wait_for_query = None
        duration = self.find_time

        def fn():
            for fn in self.attend_fns:
                fn(visual)
        self.find_buffer.set(visual, duration, "found {}".format(visual), fn)

    def wait_for(self, query=None, **kwargs):
        if not query:
            query = Query(**kwargs)
        self.start_wait_for(query)
        return self.get_found()

    def start_encode_thread(self, visual, obj, duration):
        if self.last_encode_cancel is not None:
            self.last_encode_cancel.try_cancel()

        def fn():
            self.log("encoded {}".format(obj))
            self.encode_buffer.set(obj)
            visual.set('seen', True)
            self.encode_loc = visual
            for fn in self.encode_fns:
                fn(visual, object)
        self.last_encode_cancel = self.run_can_cancel(fn, duration)

    def start_encode(self, visual, suppress_think=False):
        self.encode_buffer.acquire()
        if not suppress_think:
            self.think("encode {}".format(visual))
        obj = self.visuals[visual]
        duration = self.eyes.compute_enc_time(
            visual) if self.eyes is not None else self.default_enc_time
        if obj is not None:
            self.start_encode_thread(visual, obj, duration)
            if self.eyes is not None:
                self.eyes.prepare(visual, obj, self.time(), duration)
        else:
            self.encode_buffer.clear(duration, "encode failed")

    def get_encoded(self):
        return self.encode_buffer.get_and_release()

    def encode(self, visual):
        self.start_encode(visual)
        return self.get_encoded()

    def find_and_encode(self, query=None, **kwargs):
        if not query:
            query = Query(**kwargs)
        return self.encode(self.find(query))

    def search_for(self, query, target):
        if query is None:
            query = Query()
        query = query.eq('seen', False)
        visual = self.find(query)
        obj = self.encode(visual)
        while (visual is not None
               and obj is not None
               and not obj.equals(target)):
            visual = self.find(query)
            obj = self.encode(visual)
        if obj is not None and obj.equals(target):
            return visual
        else:
            return None


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
        sd = .1 * self.vision.display.degrees_to_pixels(self._compute_eccentricity(visual))
        new_loc = Location(visual.x + random.gauss(0, sd),
                                 visual.y + random.gauss(0, sd))
        self.log("prepare {}".format(new_loc))
        duration = self._rand_time(self.prep_time)

        def fn():
            self.move(visual, obj, new_loc, enc_start, enc_dur)
        self.last_prep_cancel = self.run_can_cancel(fn, duration)

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
        self.run(fn, duration)


class Dwell:

    def __init__(self, time, visual):
        self.time = time
        self.visual = visual
        self.duration = None


class Fixation(Dwell):

    def __init__(self, time, loc, visual):
        super().__init__(time, visual)
        self.loc = loc


class Gaze(Dwell):

    def __init__(self, fixation):
        super().__init__(fixation.time, fixation.visual)
        self.duration = fixation.duration


class EyeTracker:

    def __init__(self, eyes):
        self.eyes = eyes
        self.fixations = []
        self.eyes.add_fixate_fn(self._record)

    def _record(self, loc):
        time = self.eyes.time()
        if self.fixations:
            last = self.fixations[-1]
            last.duration = time - last.time
        visual = self.nearest_visual(loc)
        self.fixations.append(Fixation(time, loc, visual))

    def compute_gazes(self):
        gazes = []
        last = None
        for f in self.fixations:
            if last is None or not f.visual.equals(last.visual):
                last = Gaze(f)
                gazes.append(last)
            elif f.duration is not None:
                last.duration += f.duration
        return gazes

    def nearest_visual(self, loc):
        best = None
        best_d = None
        for visual in self.eyes.vision.visuals:
            d = loc.distance_to_area(visual)
            if best is None or d < best_d:
                best = visual
                best_d = d
        return best
