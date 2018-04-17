import random
import unittest
from think import Agent, Hands, Typing, Mouse, Vision, Visual, Query


class TypingTest(unittest.TestCase):

    def test_typing(self, output=False):
        agent = Agent(output=output)
        typing = Typing(Hands(agent))
        typing.type("Hello there. What's up?")
        agent.wait_for_all()
        self.assertAlmostEqual(6.597, agent.time(), 1)

    def test_timing(self, output=False):
        agent = Agent(output=output)
        typing = Typing(Hands(agent))
        self.assertAlmostEqual(6.597, typing.typing_time("Hello there. What's up?"), 1)


class MouseTest(unittest.TestCase):

    def test_mouse(self, output=False):
        agent = Agent(output=output)
        vision = Vision(agent)
        hands = Hands(agent)
        mouse = Mouse(hands, vision)
        self.button = None
        end = 20.0

        def update():
            if agent.time() < end:
                def fn():
                    vision.clear()
                    agent.wait(1.0)
                    self.button = Visual(random.randint(0, 500), random.randint(0, 500), 30, 30, 'button')
                    vision.add(self.button, "X")
                agent.run(fn)
        update()

        def fn(visual):
            if visual.equals(self.button):
                update()
        mouse.add_click_fn(fn)
        while agent.time() < end:
            visual = vision.wait_for(isa='button')
            mouse.point_and_click(visual)
        agent.wait_for_all()
        self.assertGreaterEqual(agent.time(), end)
