import random

from think import Agent, Machine, Motor, Mouse, Task, Vision, World


class ClickAMoleTask(Task):

    def __init__(self, machine):
        super().__init__()
        self.display = machine.display
        self.mouse = machine.mouse

    def run(self, time):

        def update_target():
            self.display.clear()
            self.wait(1.0)
            self.display.add_text(random.randint(0, 500), random.randint(0, 500),
                                  'X', isa='target')

        def click_target(obj):
            self.run_thread(update_target)

        self.mouse.add_click_fn(click_target)

        update_target()


class ClickAMoleAgent(Agent):

    def __init__(self, machine):
        super().__init__(output=True)
        self.vision = Vision(self, machine.display)
        self.motor = Motor(self, self.vision, machine)

    def run(self, time):
        while self.time() < time:
            visual = self.vision.wait_for(isa='target')
            self.motor.point_and_click(visual)


if __name__ == '__main__':
    machine = Machine()
    task = ClickAMoleTask(machine)
    agent = ClickAMoleAgent(machine)
    World(task, agent).run(30)
