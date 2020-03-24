import unittest

from think import Agent, Eyes, Query, Vision, Visual


class VisionTest(unittest.TestCase):

    def test_vision(self, output=False):
        agent = Agent(output=output)
        eyes = Eyes(agent)
        vision = Vision(agent, eyes)
        eyes.move_to(100, 100)
        vision.add(Visual(50, 50, 20, 20, 'text'), "Hello")
        vision.add(Visual(150, 150, 20, 20, 'text'), "Goodbye")

        self.assertEqual("Hello", vision.find_and_encode(
            Query(isa='text').lt('x', 100)))
        self.assertEqual("Goodbye", vision.find_and_encode(seen=False))

        vision.start_wait_for(isa='cross')
        agent.wait(2.0)
        vision.add(Visual(200, 200, 20, 20, 'cross'), "cross")
        self.assertEqual("cross", vision.encode(vision.get_found()))
        self.assertAlmostEqual(2.7, agent.time(), 1)
        agent.wait_for_all()
