import random
import unittest
from think import Chunk, Memory, Agent, Query


class ChunkTest(unittest.TestCase):

    def test_chunk(self):
        chunk = Chunk(slot1='val1', slot2='val2')
        self.assertEqual('val1', chunk.get('slot1'))
        self.assertEqual('val2', chunk.slot2)
        self.assertEqual('chunk', chunk.id)

        chunk.increment_use()
        self.assertEqual(1, chunk.use_count)

        chunk.add_use(2.0)
        self.assertEqual([2.0], chunk.uses)


class MemoryTest(unittest.TestCase):

    def test_memory(self):
        agent = Agent(output=False)
        memory = Memory(agent)

        memory.add(Chunk(isa='cat', name='Whiskers', owner='Jane'))
        chunk = memory.recall(Query(isa='cat'))
        self.assertEqual('Jane', chunk.get('owner'))
        self.assertEqual('Whiskers', chunk.id)

        memory.add(isa='dog', name='Spot', owner='John')
        self.assertEqual('Spot', memory.recall(isa='dog').name)
        self.assertEqual('Whiskers', memory.recall(Query().ne('isa', 'dog')).name)

        chunk = Chunk(isa='cat', name='Whiskers', owner='Jen')
        self.assertEqual('Whiskers', chunk.id)
        memory.add(chunk)
        self.assertEqual('Whiskers~2', chunk.id)
        self.assertEqual(chunk, memory.get(chunk.id))


class DecayTest(unittest.TestCase):

    def test_decay(self, output=False):
        self._test_decay(Memory.NO_DECAY, None, .100, output)
        self._test_decay(Memory.OPTIMIZED_DECAY, .817, .473, output)
        self._test_decay(Memory.ADVANCED_DECAY, .600, .815, output)

    def _test_decay(self, decay, prob, time, output):
        agent = Agent(output=output)
        memory = Memory(agent, decay)
        chunk = Chunk(isa='cat', name='Whiskers', owner='Jane')
        memory.store(chunk)
        agent.wait(.5)
        memory.rehearse(chunk)
        agent.wait(2.5)
        memory.rehearse(chunk)
        agent.wait(3.7)
        memory.rehearse(chunk)
        agent.wait(6.2)
        memory.activation_noise = 0.5
        if prob:
            self.assertAlmostEqual(prob, memory.compute_prob_recall(chunk), 2)
        self.assertAlmostEqual(memory.compute_recall_time(chunk), time, 2)
