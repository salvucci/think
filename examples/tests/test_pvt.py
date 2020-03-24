import unittest

from examples.pvt import PVTAgent, PVTTask
from think import Machine, World


class PVTTest(unittest.TestCase):

    def test_pvt(self, output=False):
        machine = Machine()
        task = PVTTask(machine)
        agent = PVTAgent(machine)
        World(task, agent).run(30, output=False)
        self.assertGreater(task.time(), 30.0)
        self.assertGreater(agent.time(), 30.0)
