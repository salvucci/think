import random

from think import Agent, Environment, Motor, Mouse, Task, Vision, World


class ClickAMoleTask(Task):

    def __init__(self, env):
        super().__init__()
        self.display = env.display
        self.mouse = env.mouse

    def run(self, time):

        def update_target():
            self.display.clear()
            self.wait(1.0)
            self.display.add_text(random.randint(0, 500), random.randint(0, 500),
                                  'X', isa='button')

        def click_target(obj):
            self.run_thread(update_target)

        self.mouse.add_click_fn(click_target)

        update_target()


class ClickAMoleAgent(Agent):

    def __init__(self, env):
        super().__init__(output=True)
        self.vision = Vision(self, env.display)
        self.motor = Motor(self, self.vision, env)

    def run(self, time):
        while self.time() < time:
            visual = self.vision.wait_for(isa='button')
            self.motor.point_and_click(visual)


if __name__ == '__main__':
    env = Environment()
    task = ClickAMoleTask(env)
    agent = ClickAMoleAgent(env)
    World(task, agent).run(30)
