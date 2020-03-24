import unittest

from examples.instructions import TypeLetterAgent, TypeLetterTask
from think import Machine, World


class VisualSearchTest(unittest.TestCase):

    def test_pvt(self, output=False):
        machine = Machine()
        task = TypeLetterTask(machine)
        agent = TypeLetterAgent(machine)
        World(task, agent).run(30, output=False)
        self.assertAlmostEqual(13.144, task.time(), 1)
        self.assertAlmostEqual(13.144, agent.time(), 1)
