import random

from think import Agent, Machine, Motor, Task, Vision, World


class VisualSearchTask(Task):

    def __init__(self, machine, n_targets=5):
        super().__init__()
        self.display = machine.display
        self.keyboard = machine.keyboard
        self.n_targets = n_targets

    def run(self, time):

        def handle_key(key):
            self.record(key)
            self.display.clear()

        self.keyboard.add_type_fn(handle_key)

        while self.time() < time:
            self.wait(10.0)
            self.display.clear()
            target_index = random.randint(0, self.n_targets)
            for i in range(self.n_targets):
                isa = 'target' if i == target_index else 'distractor'
                string = '|' if i == target_index else '-'
                self.display.add(random.randint(10, 90),
                                 random.randint(10, 90),
                                 20, 20, isa, string)
            self.record('stimulus')


class VisualSearchAgent(Agent):

    def __init__(self, machine):
        super().__init__(output=True)
        self.vision = Vision(self, machine.display)
        self.motor = Motor(self, self.vision, machine)

    def run(self, time):
        while self.time() < time:
            visual = self.vision.wait_for(seen=False)
            while (visual is not None
                    and not visual.isa == 'target'):
                self.vision.encode(visual)
                visual = self.vision.find(seen=False)
            if visual:
                self.log('target found')
                self.motor.type('j')
                self.vision.encode(visual)
            else:
                self.log('target not found')
                self.motor.type('k')


if __name__ == "__main__":
    machine = Machine()
    task = VisualSearchTask(machine)
    agent = VisualSearchAgent(machine)
    World(task, agent).run(30)
