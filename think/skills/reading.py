from think import Agent, Data, Eyes, EyeTracker, Query, Vision, Visual
from think.skills.test.test_reading import ReadingTest


class Reading:

    def test_reading(self, output=False):
        sentences = []
        for pairs in ReadingTest.SENTENCES:
            sentences.append(ReadingTest.Sentence(pairs))
        self.gaze_dur = Data(5)
        self.ff_dur = Data(5)
        self.skip_prob = Data(5)
        for _ in range(ReadingTest.N_SIMULATIONS):
            for sentence in sentences:
                self.run_trial(sentence)
        result_gaze_dur = self.gaze_dur.analyze(ReadingTest.HUMAN_GAZE_DUR)
        result_ff_dur = self.ff_dur.analyze(ReadingTest.HUMAN_FF_DUR)
        result_skip_prob = self.skip_prob.analyze(ReadingTest.HUMAN_SKIP_PROB)
        if output:
            result_gaze_dur.output("Gaze Durations", 0)
            result_ff_dur.output("First Fixation Durations", 0)
            result_skip_prob.output("Skip Probabilities", 2)
        self.assertGreaterEqual(result_gaze_dur.r, .80)
        self.assertGreaterEqual(result_ff_dur.r, .80)
        self.assertGreaterEqual(result_skip_prob.r, .80)
        self.assertLessEqual(result_gaze_dur.nrmse, .20)
        self.assertLessEqual(result_ff_dur.nrmse, .20)
        self.assertLessEqual(result_skip_prob.nrmse, .80)

    class Word:
        def __init__(self, string, freq):
            self.string = string
            self.freq = freq

    class Sentence:
        def __init__(self, pairs):
            self.words = []
            for pair in pairs:
                self.words.append(ReadingTest.Word(pair[0], pair[1] / 1e6))

    def run_trial(self, sentence):
        agent = Agent(output=False)
        eyes = Eyes(agent)
        vision = Vision(agent, eyes)
        tracker = EyeTracker(eyes)
        self.add_visuals(sentence, vision)
        self.read_sentence(agent, vision)
        agent.wait_for_all()
        self.analyze_trial(sentence, tracker)

    def add_visuals(self, sentence, vision):
        spc = 16
        x = 50
        y = 50
        h = spc
        for word in sentence.words:
            w = spc * len(word.string)
            visual = Visual(x + w / 2, y + h / 2, w, h, 'word')
            visual.freq = word.freq
            visual.set('data', word)
            vision.add(visual, word.string)
            x += w + spc

    def read_sentence(self, agent, vision):
        vision.eyes.move_to(0, 50)
        visual = vision.find(isa='word')
        while visual:
            vision.encode(visual)
            agent.wait(ReadingTest.RECALL_DURATION)
            visual = vision.find(isa='word', seen=False)

    def compute_freq_class(self, word):
        if word.freq < .000010:
            return 1
        elif word.freq < .000100:
            return 2
        elif word.freq < .001000:
            return 3
        elif word.freq < .010000:
            return 4
        else:
            return 5

    def analyze_trial(self, sentence, tracker):
        gazes = tracker.compute_gazes()
        if len(gazes) > 0:
            del gazes[0]
        for gaze in gazes:
            word = gaze.visual.get('data')
            if word and gaze.duration:
                dur = 1000 * gaze.duration
                self.gaze_dur.add(self.compute_freq_class(word) - 1, dur)
        fixs = tracker.fixations
        if len(fixs) > 0:
            del fixs[0]
        seen = set()
        for fix in fixs:
            word = fix.visual.get('data')
            if word and fix.duration and word not in seen:
                dur = 1000 * fix.duration
                self.ff_dur.add(self.compute_freq_class(word) - 1, dur)
                seen.add(word)
        for word in sentence.words:
            skipped = True
            for gaze in gazes:
                gaze_word = gaze.visual.get('data')
                if word == gaze_word:
                    skipped = False
            self.skip_prob.add(self.compute_freq_class(
                word) - 1, 1 if skipped else 0)
