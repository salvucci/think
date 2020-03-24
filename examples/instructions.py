from think import Agent, Memory, Aural, Audition, Vision, Item, Visual, Query, Language, Instruction, Typing, Motor


class TypeLetterAgent(Agent):

    def __init__(self):
        super().__init__(output=True)
        self.vision = Vision(self)
        self.memory = Memory(self)
        self.audition = Audition(self)
        self.typing = Typing(Motor(self))

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
                self.typing.type(context.get(action.object))

        self.instruction = Instruction(
            self, self.memory, self.audition, self.language)
        self.instruction.add_executor(executor)


class TypeLetterTask:

    def run(self, agent):
        vision = agent.vision
        audition = agent.audition
        typing = agent.typing
        instruction = agent.instruction

        typed = []

        def type_handler(key):
            typed.append(key)
        typing.add_type_fn(type_handler)

        vision.add(Visual(50, 50, 20, 20, 'text'), 'a')
        pointer = Visual(50, 50, 1, 1, 'pointer')
        vision.add(pointer, 'pointer')

        speech = [
            'to type',
            ['read letter', (50, 50)],
            'type letter',
            'done'
        ]

        def stimulus_thread():
            for line in speech:
                agent.wait(3.0)
                if isinstance(line, str):
                    audition.add(Aural(isa='speech'), line)
                else:
                    audition.add(Aural(isa='speech'), line[0])
                    loc = line[1]
                    pointer.move(loc[0], loc[1])
        agent.run(stimulus_thread)

        goal = instruction.listen_and_learn()
        instruction.execute(goal)

        agent.wait_for_all()
        print(typed)


if __name__ == "__main__":
    TypeLetterTask().run(TypeLetterAgent())
