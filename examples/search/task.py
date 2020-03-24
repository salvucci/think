import random

from think import (Agent, Audition, Aural, Motor, Instruction, Item, Language,
                   Memory, Query, Task, Typing, Vision, Visual, World)


class SearchTask(Task):
    """Visual Search Task"""

    def __init__(self, agent, instructions=[], n_targets=5):
        super().__init__(agent)
        self.vision = self.agent.vision
        self.audition = self.agent.audition
        self.typing = self.agent.typing
        self.instructions = instructions
        self.n_targets = n_targets

    def run(self, time=10):

        def handle_key(key):
            self.vision.clear()
            self.record('response')

        self.typing.add_type_fn(handle_key)

        for line in self.instructions:
            self.wait(5.0)
            if isinstance(line, str):
                self.audition.add(Aural(isa='speech'), line)
            else:
                self.audition.add(Aural(isa='speech'), line[0])
                # loc = line[1]
                # pointer.move(loc[0], loc[1])

        while self.time() < time:
            self.wait(10)
            # allow for index self.n_targets for target not present
            target_index = random.randint(0, self.n_targets)
            for i in range(self.n_targets):
                isa = 'vertical-line' if i == target_index else 'distractor'
                string = '|' if i == target_index else '-'
                self.vision.add(Visual(random.randint(10, 90), random.randint(10, 90),
                                       20, 20, isa), string)
            self.record('stimulus')
