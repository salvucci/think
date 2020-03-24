from think import Agent, Audition, Motor, Typing, Vision, Visual


class PVTAgent(Agent):

    def __init__(self):
        """Initializes the agent"""
        super().__init__(output=True)
        self.vision = Vision(self)
        self.audition = Audition(self)
        self.typing = Typing(Motor(self))

    def run(self, time=300):
        while self.time() < time:
            visual = self.vision.wait_for(seen=False)
            self.vision.start_encode(visual)
            self.typing.type('j')
            self.vision.get_encoded()
