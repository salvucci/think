import unittest
from think import Agent, Audition, Aural, Query


class AuditionTest(unittest.TestCase):

    def test_audition(self, output=True):
        agent = Agent(output=output)
        aud = Audition(agent)

        aural = Aural('word')
        aud.add(aural, "Hello")
        aural2 = aud.listen_for(isa='word')
        self.assertEqual(aural, aural2)

        aud.add_speech("Looks like this is working.")
        for _ in range(5):
            word = aud.listen_for_and_encode(isa='word')
            print(word)

        # aud.add(Aural('word'), "Hello")
        # aud.add(Aural('word'), "Goodbye")

        # self.assertEqual("Hello", aud.find_and_encode(
        #     Query(isa='text').lt('x', 100)))
        # self.assertEqual("Goodbye", aud.find_and_encode(seen=False))

        # aud.start_wait_for(isa='cross')
        # agent.wait(2.0)
        # aud.add(Aural(200, 200, 20, 20, 'cross'), "cross")
        # self.assertEqual("cross", aud.encode(aud.get_found()))
        # self.assertAlmostEqual(2.7, agent.time(), 1)
        agent.wait_for_all()
