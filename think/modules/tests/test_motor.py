import random
import unittest

from think import Agent, Machine, Motor, Query, Vision, Visual


class TypingTest(unittest.TestCase):

    def test_typing(self, output=False):
        agent = Agent(output=output)
        machine = Machine()
        vision = Vision(agent, machine.display)
        motor = Motor(agent, vision, machine)
        motor.type('Hello there. What\'s up?')
        agent.wait_for_all()
        self.assertAlmostEqual(6.597, agent.time(), 1)

    def test_timing(self, output=False):
        agent = Agent(output=output)
        machine = Machine()
        vision = Vision(agent, machine.display)
        motor = Motor(agent, vision, machine)
        self.assertAlmostEqual(6.597, motor.typing_time(
            'Hello there. What\'s up?'), 1)


class MouseTest(unittest.TestCase):

    def test_mouse(self, output=False):
        agent = Agent(output=output)
        machine = Machine()
        vision = Vision(agent, machine.display)
        motor = Motor(agent, vision, machine)
        self.button = None
        end = 20.0

        def update():
            if agent.time() < end:
                def fn():
                    vision.clear()
                    agent.wait(1.0)
                    self.button = machine.display.add(
                        random.randint(0, 500), random.randint(0, 500),
                        30, 30, 'button', 'X')
                agent.run_thread(fn)

        update()

        def fn(obj):
            if obj == 'X':
                update()

        machine.mouse.add_click_fn(fn)
        while agent.time() < end:
            visual = vision.wait_for(isa='button')
            motor.point_and_click(visual)
        agent.wait_for_all()
        self.assertGreaterEqual(agent.time(), end)
