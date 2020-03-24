import unittest

from think import Agent, Audition, Aural, Query


class AuditionTest(unittest.TestCase):

    def test_audition(self, output=False):
        agent = Agent(output=output)
        audition = Audition(agent)

        word = 'Hello'
        aural = Aural('word')
        audition.add(aural, word)
        aural2 = audition.listen(isa='word')
        self.assertEqual(aural, aural2)
        word2 = audition.encode(aural2)
        self.assertEqual(word, word2)

        text = 'Looks like this is working'
        audition.add_speech(text)
        word = audition.listen_and_encode(isa='word')
        heard = []
        while word is not None:
            heard.append(word)
            word = audition.listen_and_encode(isa='word')
        self.assertEqual(text, ' '.join(heard))

        agent.wait_for_all()
