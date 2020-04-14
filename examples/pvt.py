import random

from think import Agent, Environment, Motor, Task, Vision, World


class PVTTask(Task):

    def __init__(self, env):
        super().__init__()
        self.display = env.display
        self.keyboard = env.keyboard

    def run(self, time):

        def handle_key(key):
            self.display.clear()

        self.keyboard.add_type_fn(handle_key)

        while self.time() < time:
            self.wait(random.randint(2.0, 10.0))
            self.display.add_text(50, 50, 'X')


class PVTAgent(Agent):

    def __init__(self, env):
        super().__init__(output=True)
        self.vision = Vision(self, env.display)
        self.motor = Motor(self, self.vision, env)

    def run(self, time):
        while self.time() < time:
            visual = self.vision.wait_for(seen=False)
            self.vision.start_encode(visual)
            self.motor.type('j')
            self.vision.get_encoded()


if __name__ == '__main__':
    env = Environment()
    task = PVTTask(env)
    agent = PVTAgent(env)
    World(task, agent).run(30)
