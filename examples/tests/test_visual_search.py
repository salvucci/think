import unittest

from examples.visual_search import VisualSearchAgent, VisualSearchTask
from think import Environment, World


class VisualSearchTest(unittest.TestCase):

    def test_pvt(self, output=False):
        env = Environment()
        task = VisualSearchTask(env)
        agent = VisualSearchAgent(env)
        World(task, agent).run(30, output=False)
        self.assertGreater(task.time(), 30.0)
        self.assertGreater(agent.time(), 30.0)
