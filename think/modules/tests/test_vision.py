import unittest

from think import Agent, Eyes, Machine, Query, Vision, Visual


class VisionTest(unittest.TestCase):

    def test_vision(self, output=False):
        agent = Agent(output=output)
        display = Machine().display
        eyes = Eyes(agent)
        vision = Vision(agent, display, eyes)
        eyes.move_to(100, 100)
        display.add_text(50, 50, 'Hello')
        display.add_text(150, 150, 'Goodbye')

        self.assertEqual("Hello", vision.find_and_encode(
            Query(isa='text').lt('x', 100)))
        self.assertEqual("Goodbye", vision.find_and_encode(seen=False))

        vision.start_wait_for(isa='cross')
        agent.wait(2.0)
        display.add(200, 200, 20, 20, 'cross', "cross")
        self.assertEqual("cross", vision.encode(vision.get_found()))
        self.assertAlmostEqual(2.7, agent.time(), 1)
        agent.wait_for_all()
