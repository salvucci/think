import unittest

from think import Agent, Data, Eyes, EyeTracker, Query, Vision, Visual


class ReadingTest(unittest.TestCase):
    N_SIMULATIONS = 20
    RECALL_DURATION = .060
    HUMAN_GAZE_DUR = [293, 272, 256, 234, 214]
    HUMAN_FF_DUR = [248, 233, 230, 223, 208]
    HUMAN_SKIP_PROB = [.10, .13, .22, .55, .67]

    SENTENCES = [
        [("margie", 1), ("moved", 181), ("into", 1789), ("her", 3036), ("new", 1635),
         ("apartment", 81), ("at", 5372), ("the",
                                           69974), ("end", 409), ("of", 36414),
         ("the", 69974), ("summer", 134)],
        [("the", 69974), ("principal", 92), ("introduced", 52), ("the", 69974), ("new", 1635),
         ("president", 382), ("of", 36414), ("the", 69974), ("junior", 75), ("class", 207)],
        [("none", 108), ("of", 36414), ("the", 69974), ("students", 213), ("wanted", 226),
         ("to", 26155), ("have", 3942), ("an",
                                         3727), ("exam", 1), ("after", 1068),
         ("spring", 126), ("break", 88)],
        [("mark", 83), ("told", 413), ("janet", 1), ("that", 10593), ("he", 9547), ("would", 2715),
         ("meet", 149), ("her", 3036), ("after", 1068), ("baseball", 57), ("practice", 94)],
        [("bill", 143), ("complained", 22), ("that", 10593), ("the", 69974), ("magazine", 39),
         ("included", 97), ("more", 2214), ("ads", 10), ("than", 1790), ("articles", 31)],
        [("the", 69974), ("angry", 45), ("man", 1207), ("called", 401), ("the", 69974),
         ("senator", 40), ("to", 26155), ("complain",
                                          11), ("about", 1814), ("the", 69974),
         ("new", 1635), ("tax", 201), ("law", 299)],
        [("the", 69974), ("policeman", 19), ("demanded", 102), ("to", 26155), ("see", 772),
         ("jims", 4), ("license", 36), ("and", 28850), ("registration", 23)],
        [("a", 23127), ("strict", 11), ("vegetarian", 1), ("jennifer", 1), ("does", 485),
         ("not", 4868), ("eat", 61), ("chicken", 37), ("or", 4204), ("beef", 31)],
        [("nancys", 1), ("kitchen", 90), ("was", 9816), ("infested", 1), ("with", 7289),
         ("carpenter", 6), ("ants", 1), ("and", 28850), ("roaches", 1)],
        [("the", 69974), ("hurricane", 8), ("destroyed", 39), ("houses", 83), ("in", 21335),
         ("the", 69974), ("village", 72), ("and",
                                           28850), ("left", 141), ("many", 1029),
         ("homeless", 1)],
        [("amy", 15), ("told", 413), ("the", 69974), ("teacher", 80), ("that", 10593), ("her", 3036),
         ("dog", 76), ("ate", 16), ("her", 3036), ("homework", 1), ("assignment", 62)],
        [("ed", 13), ("was", 9816), ("forbidden", 15), ("to", 26155), ("attend", 54), ("college", 267),
         ("parties", 59), ("while", 680), ("he",
                                           9547), ("was", 9816), ("in", 21335),
         ("high", 498), ("school", 493)],
        [("sheri", 1), ("and", 28850), ("her", 3036), ("friends", 161), ("went", 508), ("to", 26155),
         ("hawaii", 16), ("for", 9489), ("their", 2670), ("summer", 134), ("vacation", 47)],
        [("mark", 83), ("put", 438), ("too", 834), ("much", 937), ("soap", 22), ("in", 21335),
         ("the", 69974), ("washing", 44), ("machine",
                                           103), ("and", 69974), ("it", 8761),
         ("overflowed", 2)],
        [("the", 69974), ("circus", 7), ("tents", 10), ("were", 3286), ("crowded", 32), ("with", 7289),
         ("animals", 58), ("clowns", 2), ("and", 28850), ("children", 355)],
        [("the", 69974), ("bear", 57), ("chased", 1), ("after", 1068), ("the", 69974), ("forest", 66),
         ("ranger", 2), ("who", 2252), ("was", 9816), ("carrying", 71), ("honey", 24)],
        [("the", 69974), ("best", 351), ("place", 570), ("that", 10593), ("serves", 37),
         ("coffee", 78), ("and", 28850), ("muffins",
                                          1), ("is", 10109), ("dunkin", 1),
         ("donuts", 1)],
        [("mr", 845), ("jones", 72), ("asked", 398), ("his", 6994), ("son", 165), ("to", 26155),
         ("water", 445), ("the", 69974), ("plants",
                                          59), ("and", 28850), ("mow", 1),
         ("the", 69974), ("lawn", 15)],
        [("the", 69974), ("brides", 5), ("mother", 216), ("cried", 30), ("during", 585),
         ("the", 69974), ("entire", 32), ("wedding", 18)],
        [("the", 69974), ("drunk", 36), ("driver", 49), ("lost", 173), ("control", 223),
         ("crashed", 12), ("into", 1789), ("a",
                                           23127), ("street", 244), ("sign", 94),
         ("and", 28850), ("died", 86)],
        [("mary", 87), ("was", 9816), ("the", 69974), ("only", 1748), ("teenager", 4), ("who", 2252),
         ("attended", 36), ("the", 69974), ("square",
                                            143), ("dance", 90), ("in", 21335),
         ("town", 212)],
        [("the", 69974), ("burglar", 1), ("broke", 67), ("the", 69974), ("window", 119),
         ("and", 28850), ("quietly", 49), ("sneaked",
                                           6), ("into", 1789), ("the", 69974),
         ("house", 591)],
        [("jimmy", 11), ("was", 9816), ("sent", 145), ("to", 26155), ("the", 69974), ("principals", 1),
         ("office", 255), ("because", 883), ("he", 9547), ("punched", 1), ("sally", 14)],
        [("most", 1159), ("job", 239), ("applications", 25), ("require", 86), ("at", 5372),
         ("least", 343), ("one", 3297), ("letter", 145), ("of", 36414), ("recommendation", 24)],
        [("the", 69974), ("daredevil", 1), ("was", 9816), ("relieved", 24), ("when", 2333),
         ("his", 6994), ("parachute", 1), ("finally", 191), ("opened", 131)],
        [("it", 8761), ("is", 10109), ("not", 4868), ("unusual", 63), ("to", 26155), ("see", 772),
         ("an", 3727), ("armadillo", 2), ("cross",
                                          55), ("a", 23127), ("road", 195),
         ("in", 21335), ("texas", 69)],
        [("erik", 1), ("took", 426), ("his", 6995), ("sick", 51), ("parakeet", 1), ("to", 26155),
         ("the", 69974), ("veterinarian", 2), ("on", 6740), ("tuesday", 58)],
        [("al", 14), ("stretched", 34), ("before", 1015), ("running", 123), ("to", 26155),
         ("avoid", 58), ("pulling", 25), ("a",
                                          23127), ("ligament", 1), ("or", 4204),
         ("muscle", 42)],
        [("the", 69974), ("boxer", 1), ("flared", 5), ("his", 6994), ("nostrils", 3), ("as", 7251),
         ("he", 9547), ("entered", 97), ("the", 69974), ("boxing", 1), ("ring", 47)],
        [("mary", 87), ("was", 9816), ("thrilled", 3), ("to", 26155), ("receive", 76), ("a", 23127),
         ("trinket", 1), ("from", 4371), ("her", 3036), ("boyfriend", 1)],
        [("covered", 104), ("with", 7289), ("maggots", 2), ("the", 69974), ("rug", 10), ("was", 9816),
         ("removed", 75), ("from", 4371), ("the",
                                           69974), ("smelly", 1), ("dorm", 1),
         ("room", 384)],
        [("propelled", 1), ("from", 4371), ("a", 23127), ("submarine", 26), ("the", 69974),
         ("torpedo", 1), ("struck", 59), ("the", 69974), ("battleship", 1)],
        [("alfred", 52), ("served", 119), ("baked", 8), ("haddock", 1), ("and", 28850),
         ("asparagus", 1), ("to", 26155), ("his", 6994), ("girlfriend", 1)],
        [("the", 69974), ("dancer", 31), ("resembled", 8), ("a", 23127), ("gazelle", 1), ("as", 7251),
         ("he", 9547), ("leaped", 20), ("across", 282), ("the", 69974), ("stage", 175)],
        [("the", 69974), ("little", 831), ("girl", 220), ("had", 5134), ("dimples", 1), ("in", 21335),
         ("her", 3036), ("chin", 25), ("and", 28850), ("a",
                                                       23127), ("freckle", 1), ("on", 6740),
         ("her", 3036), ("nose", 60)],
        [("the", 69974), ("beach", 61), ("was", 9816), ("covered", 104), ("with", 7289),
         ("pebbles", 3), ("sea", 93), ("shells", 15), ("and", 28850), ("star", 1)],
        [("the", 69974), ("child", 213), ("had", 5134), ("a", 23127), ("nightmare", 9),
         ("about", 1814), ("being", 681), ("chased",
                                           1), ("by", 5305), ("hornets", 1),
         ("and", 28850), ("wasps", 1)],
        [("biff", 1), ("dove", 4), ("into", 1789), ("the", 69974), ("water", 445), ("and", 28850),
         ("retrieved", 10), ("a", 23127), ("scallop",
                                           1), ("from", 4371), ("the", 69974),
         ("ocean", 34), ("floor", 158)],
        [("the", 69974), ("little", 831), ("girl", 220), ("picked", 78), ("all", 3001), ("the", 36414),
         ("cashews", 69974), ("out", 1), ("of",
                                          2096), ("the", 36414), ("trail", 69974),
         ("mix", 31)],
        [("the", 69974), ("athlete", 9), ("broke", 67), ("his", 6994), ("pelvis", 1), ("and", 28850),
         ("could", 1601), ("not", 4868), ("participate",
                                          22), ("in", 21335), ("the", 69974),
         ("race", 103)],
        [("the", 69974), ("game", 123), ("show", 288), ("contestant", 1), ("won", 68), ("a", 23127),
         ("quartz", 1), ("watch", 81), ("and",
                                        28850), ("a", 23127), ("television", 51),
         ("set", 414)],
        [("the", 69974), ("careless", 8), ("mailman", 1), ("delivered", 37), ("the", 69974),
         ("parcel", 1), ("to", 26155), ("the", 69974), ("wrong", 129), ("house", 591)],
        [("after", 1068), ("receiving", 34), ("money", 265), ("the", 69974), ("beggar", 2),
         ("bought", 56), ("cigarettes", 12), ("and",
                                              28850), ("a", 23127), ("case", 362),
         ("of", 36414), ("beer", 35)],
        [("at", 5372), ("the", 69974), ("science", 131), ("party", 216), ("people", 847),
         ("were", 3286), ("dressed", 36), ("as",
                                           7251), ("robots", 3), ("and", 28850),
         ("computers", 5)],
        [("the", 69974), ("stunning", 6), ("actress", 6), ("wore", 65), ("a", 23127), ("black", 203),
         ("sequin", 1), ("dress", 67), ("to",
                                        26155), ("the", 69974), ("award", 46),
         ("ceremony", 18)],
        [("when", 2333), ("the", 69974), ("man", 1207), ("ran", 134), ("in", 21335), ("the", 69974),
         ("blizzard", 7), ("an", 3727), ("icicle",
                                         1), ("formed", 76), ("on", 6740),
         ("his", 6994), ("beard", 26)],
        [("the", 69974), ("clumsy", 6), ("assistant", 36), ("dropped", 101), ("a", 23127),
         ("beaker", 2), ("and", 28850), ("it",
                                         8761), ("shattered", 13), ("on", 6740),
         ("the", 69974), ("floor", 158)],
        [("when", 2333), ("als", 2), ("retina", 1), ("became", 246), ("inflamed", 1), ("and", 28850),
         ("sore", 10), ("he", 9547), ("visited",
                                      41), ("the", 69974), ("eye", 122),
         ("doctor", 100)]
    ]

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
