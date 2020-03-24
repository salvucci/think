import unittest

from think import Agent, Memory, Speech


class AgentTest(unittest.TestCase):

    def test_agent(self, output=False):
        agent = Agent(output=output)
        agent.wait(10.0)
        self.assertAlmostEqual(10.0, agent.time(), 2)
        agent.run_thread(lambda: agent.wait(5.0))
        agent.wait(2.0)
        self.assertAlmostEqual(12.0, agent.time(), 2)
        agent.wait_for_all()
        self.assertAlmostEqual(15.0, agent.time(), 2)

    def test_threads(self, output=False):
        agent = Agent(output=output)
        memory = Memory(agent)
        memory.add(isa='item')
        memory.add(isa='digit', value=1)
        memory.add(isa='number', value='three')
        speech = Speech(agent)

        def thread2():
            for _ in range(2):
                number = memory.recall(isa='number')
                speech.say(number.value)
        agent.run_thread(thread2)
        agent.wait(.100)

        def thread3():
            for _ in range(2):
                memory.recall('digit')
        agent.run_thread(thread3)
        for _ in range(2):
            memory.recall('item')
        agent.wait_for_all()
        self.assertAlmostEqual(1.200, agent.time(), 2)
