
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
