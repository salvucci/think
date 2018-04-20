from think import Agent, Memory, Speech


class Arithmetic:

    def __init__(self, agent, memory, speech):
        self.agent = agent
        self.memory = memory
        self.speech = speech
        for i in range(0, 100):
            self.memory.add(isa='count', i=i, next=(i + 1))
        for i in range(0, 13):
            for j in range(0, 13):
                self.memory.add(isa='sum', i=i, j=j, sum=(i + j))
                self.memory.add(isa='product', i=i, j=j, product=(i * j))

    def count_to(self, n):
        count = 0
        while count < n:
            count = self.memory.recall(isa='count', i=count).next
            self.speech.subvocalize(count)

    def next(self, i):
        return self.memory.recall(isa='count', i=i).next

    def add(self, i, j):
        return self.memory.recall(isa='sum', i=i, j=j).sum

    def multiply(self, i, j):
        return self.memory.recall(isa='product', i=i, j=j).product


if __name__ == "__main__":
    agent = Agent(output=True)
    memory = Memory(agent)
    speech = Speech(agent)
    arithmetic = Arithmetic(agent, memory, speech)
    arithmetic.count_to(5)
    speech.say(arithmetic.multiply(8, 11))
    agent.wait_for_all()
