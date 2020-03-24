import random
import unittest
from think import Memory, Agent, Vision, Visual, Typing, Motor, Data


class PairedAssociatesTest(unittest.TestCase):
    N_SIMULATIONS = 20
    N_BLOCKS = 8
    HUMAN_CORRECT = [.000, .526, .667, .798, .887, .924, .958, .954]
    HUMAN_RT = [.000, 2.158, 1.967, 1.762, 1.680, 1.552, 1.467, 1.402]
    PAIRS = [("bank", 0), ("card", 1), ("dart", 2), ("face", 3), ("game", 4),
             ("hand", 5), ("jack", 6), ("king", 7), ("lamb", 8), ("mask", 9),
             ("neck", 0), ("pipe", 1), ("quip", 2), ("rope", 3), ("sock", 4),
             ("tent", 5), ("vent", 6), ("wall", 7), ("xray", 8), ("zinc", 9)]

    def test_paired_associates(self, output=False):
        self.correct = Data(PairedAssociatesTest.N_BLOCKS)
        self.rt = Data(PairedAssociatesTest.N_BLOCKS)
        for _ in range(PairedAssociatesTest.N_SIMULATIONS):
            self.run_trial()
        result_correct = self.correct.analyze(
            PairedAssociatesTest.HUMAN_CORRECT)
        if output:
            result_correct.output("Correctness", 2)
        result_rt = self.rt.analyze(PairedAssociatesTest.HUMAN_RT)
        if output:
            result_rt.output("Response Times", 2)
        self.assertGreater(result_correct.r, .80)
        self.assertGreater(result_rt.r, .80)
        self.assertLess(result_correct.nrmse, .20)
        self.assertLess(result_rt.nrmse, .20)

    def run_trial(self):
        agent = Agent(output=False)
        memory = Memory(agent, Memory.OPTIMIZED_DECAY)
        memory.decay_rate = .5
        memory.activation_noise = .5
        memory.retrieval_threshold = -1.8
        memory.latency_factor = .450
        vision = Vision(agent)
        typing = Typing(Motor(agent))
        self.trial_start = 0
        self.block_index = 0

        def fn():
            for i in range(PairedAssociatesTest.N_BLOCKS):
                self.block_index = i
                pairs = PairedAssociatesTest.PAIRS.copy()
                random.shuffle(pairs)
                for pair in pairs:
                    self.trial_start = agent.time()
                    vision.clear().add(Visual(50, 50, 20, 20, 'word'), pair[0])
                    agent.wait(5.0)
                    vision.clear().add(
                        Visual(50, 50, 20, 20, 'digit'), pair[1])
                    agent.wait(5.0)
        agent.run(fn)

        def type_fn(c):
            self.rt.add(self.block_index, agent.time() - self.trial_start)
        typing.add_type_fn(type_fn)
        for i in range(PairedAssociatesTest.N_BLOCKS):
            for _ in range(len(PairedAssociatesTest.PAIRS)):
                word = vision.encode(vision.wait_for(isa='word'))
                chunk = memory.recall(word=word)
                if chunk:
                    typing.type(chunk.get('digit'))
                    self.correct.add(i, 1)
                else:
                    self.correct.add(i, 0)
                digit = vision.encode(vision.wait_for(isa='digit'))
                memory.store(word=word, digit=digit)
        agent.wait_for_all()
