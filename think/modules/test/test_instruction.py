import unittest
from think import Agent, Memory, Aural, Audition, Vision, Visual, Query, Language, Instruction, Typing, Hands


class InstructionTest(unittest.TestCase):

    def test_instruction_type(self, output=False):
        agent = Agent(output=output)
        vision = Vision(agent)
        language = Language(agent, vision)
        memory = Memory(agent)
        audition = Audition(agent)
        typing = Typing(Hands(agent))
        instruction = Instruction(agent, memory, audition, language)
        typed = []

        def type_handler(key):
            typed.append(key)
        typing.add_type_fn(type_handler)

        def read_executor(step, context):
            obj = step.obj
            query = Query(x=step.x, y=step.y)
            context.set(obj, vision.find_and_encode(query))
        instruction.set_executor('read', read_executor)

        def type_executor(step, context):
            obj = step.obj
            typing.type(context.get(obj))
        instruction.set_executor('type', type_executor)

        vision.add(Visual(50, 50, 20, 20, 'text'), 'a')
        pointer = Visual(50, 50, 1, 1, 'pointer')
        vision.add(pointer, 'pointer')

        speech = [
            'to type',
            ['read letter', (50, 50)],
            'type letter',
            'done'
        ]

        def thread():
            for line in speech:
                agent.wait(3.0)
                if isinstance(line, str):
                    audition.add(Aural(isa='speech'), line)
                else:
                    audition.add(Aural(isa='speech'), line[0])
                    loc = line[1]
                    pointer.move(loc[0], loc[1])
        agent.run(thread)

        goal = instruction.listen_and_learn()
        self.assertEqual('type', goal)

        context = instruction.execute(goal)
        self.assertEqual('a', context.letter)

        agent.wait_for_all()

        self.assertEqual(['a'], typed)

    def test_instruction_read(self, output=False):
        agent = Agent(output=output)
        vision = Vision(agent)
        language = Language(agent, vision)
        memory = Memory(agent)
        audition = Audition(agent)
        instruction = Instruction(agent, memory, audition, language)

        def read_executor(step, context):
            obj = step.obj
            query = Query(x=step.x, y=step.y)
            context.set(obj, vision.find_and_encode(query))
        instruction.set_executor('read', read_executor)

        equation = ['3', 'x', '/', '12', '=', '15', '/', '4']
        for i in range(0, len(equation)):
            vision.add(Visual(50 + 50 * i, 50, 20, 20, 'text'), equation[i])
        pointer = Visual(50, 50, 1, 1, 'pointer')
        vision.add(pointer, 'pointer')

        speech = [
            'to solve',
            ['read a', (50, 50)],
            ['read A', (300, 50)],
            'done'
        ]

        def thread():
            for line in speech:
                agent.wait(3.0)
                if isinstance(line, str):
                    audition.add(Aural(isa='speech'), line)
                else:
                    audition.add(Aural(isa='speech'), line[0])
                    loc = line[1]
                    pointer.move(loc[0], loc[1])
        agent.run(thread)

        goal = instruction.listen_and_learn()
        self.assertEqual('solve', goal)

        context = instruction.execute(goal)
        self.assertEqual('3', context.a)
        self.assertEqual('15', context.A)

        agent.wait_for_all()
