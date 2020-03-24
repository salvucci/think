import unittest

from think import Agent, Item, Language


class LanguageTest(unittest.TestCase):

    def test_language(self, output=False):
        agent = Agent(output=output)
        language = Language(agent)

        def interpreter(words):
            if len(words) == 2:
                return Item(isa='action', verb=words[0], object=words[1])
            else:
                return Item(isa=words[0])
        language.add_interpreter(interpreter)

        goal = language.interpret('to read')
        self.assertEqual('goal', goal.isa)
        self.assertEqual('read', goal.name)

        action = language.interpret('read a')
        self.assertEqual('action', action.isa)
        self.assertEqual('read', action.verb)
        self.assertEqual('a', action.object)

        done = language.interpret('done')
        self.assertEqual('done', done.isa)

        agent.wait_for_all()
