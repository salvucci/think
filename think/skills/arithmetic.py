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

    _num_text = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight',
                 'nine', 'ten', 'eleven', 'twelve', 'thirteen', 'fourteen', 'fifteen', 'sixteen',
                 'seventeen', 'eighteen', 'nineteen']
    _num_tens = ['', '', 'twenty', 'thirty', 'forty', 'fifty', 'sixty', 'seventy',
                 'eighty', 'ninety']

    def _num_to_text_help(self, n, divisor, unit):
        txt = self.num_to_text(n // divisor) + ' ' + unit
        rem = n % divisor
        return txt if rem == 0 else txt + ' ' + self.num_to_text(rem)

    def num_to_text(self, n):
        if n < 0:
            return 'negative ' + self.num_to_text(-n)
        elif n < 20:
            return self._num_text[n]
        elif n < 100:
            txt = self._num_tens[n // 10]
            rem = n % 10
            return txt if rem == 0 else txt + '-' + self.num_to_text(rem)
        elif n < 1000:
            return self._num_to_text_help(n, 100, 'hundred')
        elif n < 1000000:
            return self._num_to_text_help(n, 1000, 'thousand')
        else:
            return self._num_to_text_help(n, 1000000, 'million')

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


if __name__ == '__main__':
    agent = Agent(output=True)
    memory = Memory(agent)
    speech = Speech(agent)
    arithmetic = Arithmetic(agent, memory, speech)
    arithmetic.count_to(5)
    speech.say(arithmetic.multiply(8, 11))
    agent.wait_for_all()
