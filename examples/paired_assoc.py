import random

from think import Agent, Data, Machine, Memory, Motor, Task, Vision, World


class PairedAssociatesTask(Task):
    N_BLOCKS = 8
    PAIRS = [("bank", 0), ("card", 1), ("dart", 2), ("face", 3), ("game", 4),
             ("hand", 5), ("jack", 6), ("king", 7), ("lamb", 8), ("mask", 9),
             ("neck", 0), ("pipe", 1), ("quip", 2), ("rope", 3), ("sock", 4),
             ("tent", 5), ("vent", 6), ("wall", 7), ("xray", 8), ("zinc", 9)]

    def __init__(self, machine, corrects=None, rts=None):
        super().__init__()
        self.display = machine.display
        self.keyboard = machine.keyboard
        self.corrects = corrects or Data(self.N_BLOCKS)
        self.rts = rts or Data(self.N_BLOCKS)
        self.responded = False
        self.done = False

    def run(self, time):

        def handle_key(key):
            if str(key) == str(self.trial_digit):
                self.log('correct response')
                self.corrects.add(self.block, 1)
                self.rts.add(self.block, self.time() - self.trial_start)
                self.responded = True

        self.keyboard.add_type_fn(handle_key)

        for block in range(self.N_BLOCKS):
            self.block = block
            pairs = self.PAIRS.copy()
            random.shuffle(pairs)
            for word, digit in pairs:
                self.trial_start = self.time()
                self.trial_digit = digit
                self.responded = False
                self.display.clear()
                self.display.add_text(50, 50, word, isa='word')
                self.wait(5.0)
                if not self.responded:
                    self.log('incorrect response')
                    self.corrects.add(self.block, 0)
                self.display.add_text(50, 50, digit, isa='digit')
                self.wait(5.0)


class PairedAssociatesAgent(Agent):

    def __init__(self, machine, output=True):
        super().__init__(output=output)
        self.memory = Memory(self, Memory.OPTIMIZED_DECAY)
        self.vision = Vision(self, machine.display)
        self.motor = Motor(self, self.vision, machine)
        self.memory.decay_rate = .5
        self.memory.activation_noise = .5
        self.memory.retrieval_threshold = -1.8
        self.memory.latency_factor = .450

    def run(self, time):
        while self.time() < time:
            visual = self.vision.wait_for(isa='word')
            word = self.vision.encode(visual)
            chunk = self.memory.recall(word=word)
            if chunk:
                self.motor.type(chunk.get('digit'))
            visual = self.vision.wait_for(isa='digit')
            digit = self.vision.encode(visual)
            self.memory.store(word=word, digit=digit)


class PairedAssociatesSimulation():
    HUMAN_CORRECT = [.000, .526, .667, .798, .887, .924, .958, .954]
    HUMAN_RT = [.000, 2.158, 1.967, 1.762, 1.680, 1.552, 1.467, 1.402]

    def __init__(self, n_sims=10):
        self.n_sims = n_sims

    def run(self, output=False):
        corrects = Data(PairedAssociatesTask.N_BLOCKS)
        rts = Data(PairedAssociatesTask.N_BLOCKS)

        for _ in range(self.n_sims):
            machine = Machine()
            task = PairedAssociatesTask(machine, corrects=corrects, rts=rts)
            agent = PairedAssociatesAgent(machine, output=False)
            World(task, agent).run(1590)

        result_correct = corrects.analyze(self.HUMAN_CORRECT)
        result_rt = rts.analyze(self.HUMAN_RT)

        if output:
            result_correct.output("Correctness", 2)
            result_rt.output("Response Times", 2)

        return (result_correct, result_rt)


if __name__ == '__main__':

    # one simulation
    # machine = Machine()
    # task = PairedAssociatesTask(machine)
    # agent = PairedAssociatesAgent(machine)
    # World(task, agent).run(1590)

    # multiple simulations
    PairedAssociatesSimulation().run(output=True)
