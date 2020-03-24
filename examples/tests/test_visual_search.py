import unittest

from examples.visual_search import VisualSearchAgent, VisualSearchTask
from think import Machine, World


class VisualSearchTest(unittest.TestCase):

    def test_pvt(self, output=False):
        machine = Machine()
        task = VisualSearchTask(machine)
        agent = VisualSearchAgent(machine)
        World(task, agent).run(30, output=False)
        self.assertGreater(task.time(), 30.0)
        self.assertGreater(agent.time(), 30.0)
