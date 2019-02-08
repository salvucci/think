import unittest
from think import Agent, Vision, Language


class LanguageTest(unittest.TestCase):

    def test_language(self, output=False):
        agent = Agent(output=output)
        vision = Vision(agent)
        language = Language(agent, vision)

        goal = language.interpret('to read')
        self.assertEqual('goal', goal.isa)
        self.assertEqual('read', goal.name)

        action = language.interpret('read a')
        self.assertEqual('action', action.isa)
        self.assertEqual('read', action.action)
        self.assertEqual('a', action.obj)

        done = language.interpret('done')
        self.assertEqual('done', done.isa)

        agent.wait_for_all()
