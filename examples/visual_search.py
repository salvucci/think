import random

from think import Agent, Environment, Motor, Task, Vision, World


class VisualSearchTask(Task):

    def __init__(self, env, n_targets=5):
        super().__init__()
        self.display = env.display
        self.keyboard = env.keyboard
        self.n_targets = n_targets

    def run(self, time):

        def handle_key(key):
            self.display.clear()

        self.keyboard.add_type_fn(handle_key)

        while self.time() < time:
            self.wait(3.0)
            self.display.clear()
            target_index = random.randint(0, self.n_targets)
            for i in range(self.n_targets):
                string = 'C' if i == target_index else 'O'
                self.display.add_text(random.randint(10, 90),
                                      random.randint(10, 90), string)


class VisualSearchAgent(Agent):

    def __init__(self, env):
        super().__init__(output=True)
        self.vision = Vision(self, env.display)
        self.motor = Motor(self, self.vision, env)

    def run(self, time):
        while self.time() < time:
            visual = self.vision.wait_for(seen=False)
            obj = self.vision.encode(visual) if visual else None
            while visual and obj != 'C':
                visual = self.vision.find(seen=False)
                obj = self.vision.encode(visual) if visual else None
            if obj == 'C':
                self.log('target found')
                self.motor.type('j')
                self.vision.encode(visual)
            else:
                self.log('target not found')
                self.motor.type('k')


if __name__ == '__main__':
    env = Environment()
    task = VisualSearchTask(env)
    agent = VisualSearchAgent(env)
    World(task, agent).run(30)
