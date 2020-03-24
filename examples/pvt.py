import random

from think import Agent, Machine, Motor, Task, Vision, World


class PVTTask(Task):

    def __init__(self, machine):
        super().__init__()
        self.display = machine.display
        self.keyboard = machine.keyboard

    def run(self, time):

        def handle_key(key):
            self.display.clear()
            self.record('response')

        self.keyboard.add_type_fn(handle_key)

        while self.time() < time:
            self.wait(random.randint(2.0, 10.0))
            self.display.add(50, 50, 20, 20, 'stimulus', 'X')
            self.record('stimulus')


class PVTAgent(Agent):

    def __init__(self, machine):
        super().__init__(output=True)
        self.vision = Vision(self, machine.display)
        self.motor = Motor(self, self.vision, machine)

    def run(self, time):
        while self.time() < time:
            visual = self.vision.wait_for(seen=False)
            self.vision.start_encode(visual)
            self.motor.type('j')
            self.vision.get_encoded()


if __name__ == "__main__":
    machine = Machine()
    agent = PVTAgent(machine)
    task = PVTTask(machine)
    World(task, agent).run(30)
