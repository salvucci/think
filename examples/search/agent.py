from think import Agent, Audition, Hands, Typing, Vision, Visual


class SearchAgent(Agent):

    def __init__(self):
        super().__init__(output=True)
        self.vision = Vision(self)
        self.audition = Audition(self)
        self.typing = Typing(Hands(self))

    def run(self, time=300):
        while self.time() < time:
            visual = self.vision.wait_for(seen=False)
            while (visual is not None
                    and not visual.isa == 'vertical-line'):
                obj = self.vision.encode(visual)
                print('**** skip')
                visual = self.vision.find(seen=False)
            if visual:
                print('**** found')
                self.typing.type('j')
                self.vision.encode(visual)
            else:
                print('**** not found')
                self.typing.type('k')
