from think import (Agent, Audition, Aural, Environment, Instruction, Item,
                   Language, Memory, Motor, Query, Task, Vision, Visual, World)


class TypeLetterTask(Task):

    def __init__(self, env):
        super().__init__()
        self.display = env.display
        self.speakers = env.speakers
        self.keyboard = env.keyboard

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

    def __init__(self, env, output=True):
        super().__init__(output=output)
        self.memory = Memory(self)
        self.vision = Vision(self, env.display)
        self.audition = Audition(self, env.speakers)
        self.motor = Motor(self, self.vision, env)

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


if __name__ == '__main__':
    env = Environment()
    task = TypeLetterTask(env)
    agent = TypeLetterAgent(env)
    World(task, agent).run(30)
