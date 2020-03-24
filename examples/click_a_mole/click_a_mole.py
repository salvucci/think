import random
from think import Agent, Vision, Visual, Hands, Mouse


class ClickAMole:

    def __init__(self, agent, vision, mouse):
        self.agent = agent
        self.vision = vision
        self.mouse = mouse

    def play(self, seconds):
        self.button = None

        def update_target():
            if self.agent.time() < seconds:
                def fn():
                    self.vision.clear()
                    self.agent.wait(1.0)
                    self.button = Visual(random.randint(
                        0, 500), random.randint(0, 500), 30, 30, 'button')
                    self.vision.add(self.button, "X")
                self.agent.run(fn)
        update_target()

        def click_target(visual):
            if visual.equals(self.button):
                update_target()
        self.mouse.add_click_fn(click_target)

        while self.agent.time() < seconds:
            visual = self.vision.wait_for(isa='button')
            self.mouse.point_and_click(visual)


if __name__ == "__main__":
    agent = Agent(output=True)
    vision = Vision(agent)
    mouse = Mouse(Hands(agent, Hands.ON_MOUSE), vision)
    game = ClickAMole(agent, vision, mouse)
    game.play(20.0)
    agent.wait_for_all()
