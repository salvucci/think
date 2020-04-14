import unittest

from examples.pvt import PVTAgent, PVTTask
from think import Environment, World


class PVTTest(unittest.TestCase):

    def test_pvt(self, output=False):
        env = Environment()
        task = PVTTask(env)
        agent = PVTAgent(env)
        World(task, agent).run(30, output=False)
        self.assertGreater(task.time(), 30.0)
        self.assertGreater(agent.time(), 30.0)
