import unittest

from think import (Agent, Audition, Aural, Instruction, Item, Language,
                   Machine, Memory, Motor, Query, Vision, Visual)


class InstructionTest(unittest.TestCase):

    def test_instruction_type(self, output=False):
        agent = Agent(output=output)
        machine = Machine()
        memory = Memory(agent)
        vision = Vision(agent, machine.display)
        audition = Audition(agent, machine.speakers)
        motor = Motor(agent, vision, machine)

        def interpreter(words):
            if words[0] == 'read':
                sem = Item(isa='action', type='read', object=words[1])
                pointer = vision.find(isa='pointer')
                if pointer is not None:
                    vision.encode(pointer)
                    sem.set('x', pointer.x).set('y', pointer.y)
                return sem
            elif words[0] == 'done':
                return Item(isa='done')
            else:
                return Item(isa='action', type=words[0], object=words[1])

        language = Language(agent)
        language.add_interpreter(interpreter)

        def executor(action, context):
            if action.type == 'read':
                query = Query(x=action.x, y=action.y)
                context.set(action.object, vision.find_and_encode(query))
            elif action.type == 'type':
                motor.type(context.get(action.object))

        instruction = Instruction(agent, memory, audition, language)
        instruction.add_executor(executor)

        typed = []

        def type_handler(key):
            typed.append(key)

        machine.keyboard.add_type_fn(type_handler)

        machine.display.add_text(50, 50,'a')
        pointer = machine.display.add(50, 50, 1, 1, 'pointer', 'pointer')

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
        agent.run_thread(thread)

        goal = instruction.listen_and_learn()
        self.assertEqual('type', goal)

        context = instruction.execute(goal)
        self.assertEqual('a', context.letter)

        agent.wait_for_all()

        self.assertEqual(['a'], typed)

    def test_instruction_read(self, output=False):
        agent = Agent(output=output)
        memory = Memory(agent)
        machine = Machine()
        vision = Vision(agent, machine.display)
        audition = Audition(agent, machine.speakers)

        def interpreter(words):
            if words[0] == 'read':
                sem = Item(isa='action', type='read', object=words[1])
                pointer = vision.find(isa='pointer')
                if pointer is not None:
                    vision.encode(pointer)
                    sem.set('x', pointer.x).set('y', pointer.y)
                return sem
            elif words[0] == 'done':
                return Item(isa='done')
            else:
                return Item(isa='action', type=words[0], object=words[1])

        language = Language(agent)
        language.add_interpreter(interpreter)

        def executor(action, context):
            query = Query(x=action.x, y=action.y)
            context.set(action.object, vision.find_and_encode(query))

        instruction = Instruction(agent, memory, audition, language)
        instruction.add_executor(executor)

        equation = ['3', 'x', '/', '12', '=', '15', '/', '4']
        for i in range(0, len(equation)):
            machine.display.add_text(50 + 50 * i, 50, equation[i])
        pointer = machine.display.add(50, 50, 1, 1, 'pointer', 'pointer')

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
        agent.run_thread(thread)

        goal = instruction.listen_and_learn()
        self.assertEqual('solve', goal)

        context = instruction.execute(goal)
        self.assertEqual('3', context.a)
        self.assertEqual('15', context.A)

        agent.wait_for_all()
