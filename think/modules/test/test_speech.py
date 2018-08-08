import unittest
from think import Agent, Speech


class SpeechTest(unittest.TestCase):

    def test_speech(self, output=False):
        agent = Agent(output=output)
        speech = Speech(agent)
        speech.say("Hello I am the speech module")
        speech.subvocalize("Goodbye all")
        agent.wait_for_all()
        self.assertAlmostEqual(agent.time(), 3.650, 2)
