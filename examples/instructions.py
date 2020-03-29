from think import (Agent, Audition, Aural, Instruction, Item, Language,
                   Machine, Memory, Motor, Query, Task, Vision, Visual, World)


class TypeLetterTask(Task):

    def __init__(self, machine):
        super().__init__()
        self.display = machine.display
        self.speakers = machine.speakers
        self.keyboard = machine.keyboard

    def run(self, time):
        typed = []

        def handle_key(key):
            typed.append(key)

        self.keyboard.add_type_fn(handle_key)

        self.display.add_text(50, 50, 'a')
        pointer = self.display.add(50, 50, 1, 1, 'pointer', 'pointer')

        speech = [
            'to type',
            ['read letter', (50, 50)],
            'type letter',
            'done'
        ]

        for line in speech:
            self.wait(3.0)
            if isinstance(line, str):
                self.speakers.add('speech', line)
            else:
                self.speakers.add('speech', line[0])
                loc = line[1]
                pointer.move(loc[0], loc[1])


class TypeLetterAgent(Agent):

    def __init__(self, machine, output=True):
        super().__init__(output=output)
        self.memory = Memory(self)
        self.vision = Vision(self, machine.display)
        self.audition = Audition(self, machine.speakers)
        self.motor = Motor(self, self.vision, machine)

        def interpreter(words):
            if words[0] == 'read':
                sem = Item(isa='action', type='read', object=words[1])
                pointer = self.vision.find(isa='pointer')
                if pointer is not None:
                    self.vision.encode(pointer)
                    sem.set('x', pointer.x).set('y', pointer.y)
                return sem
            elif words[0] == 'done':
                return Item(isa='done')
            else:
                return Item(isa='action', type=words[0], object=words[1])

        self.language = Language(self)
        self.language.add_interpreter(interpreter)

        def executor(action, context):
            if action.type == 'read':
                query = Query(x=action.x, y=action.y)
                context.set(action.object, self.vision.find_and_encode(query))
            elif action.type == 'type':
                self.motor.type(context.get(action.object))

        self.instruction = Instruction(
            self, self.memory, self.audition, self.language)
        self.instruction.add_executor(executor)

    def run(self, time):
        goal = self.instruction.listen_and_learn()
        self.instruction.execute(goal)


if __name__ == "__main__":
    machine = Machine()
    task = TypeLetterTask(machine)
    agent = TypeLetterAgent(machine)
    World(task, agent).run(30)
