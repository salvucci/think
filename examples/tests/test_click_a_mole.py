import unittest

from examples.click_a_mole import ClickAMoleAgent, ClickAMoleTask
from think import Machine, World


class ClickAMoleTest(unittest.TestCase):

    def test_click_a_mole(self, output=False):
        machine = Machine()
        task = ClickAMoleTask(machine)
        agent = ClickAMoleAgent(machine)
        World(task, agent).run(30, output=False)
        self.assertGreater(task.time(), 30.0)
        self.assertGreater(agent.time(), 30.0)
