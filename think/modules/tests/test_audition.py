import unittest

from think import Agent, Audition, Aural, Environment, Query


class AuditionTest(unittest.TestCase):

    def test_audition(self, output=False):
        agent = Agent(output=output)
        speakers = Environment().speakers
        audition = Audition(agent, speakers)

        word = 'Hello'
        speakers.add('word', word)
        aural = audition.listen(isa='word')
        word2 = audition.encode(aural)
        self.assertEqual(word, word2)

        text = 'Looks like this is working'
        speakers.add_speech(text)
        word = audition.listen_and_encode(isa='word')
        heard = []
        while word is not None:
            heard.append(word)
            word = audition.listen_and_encode(isa='word')
        self.assertEqual(text, ' '.join(heard))

        agent.wait_for_all()
