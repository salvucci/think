from think import Agent, Memory, Aural, Audition, Vision, Visual, Query, Language, Instruction, Typing, Hands


class TypeLetterAgent(Agent):

    def __init__(self):
        super().__init__(output=True)
        self.vision = Vision(self)
        self.language = Language(self, self.vision)
        self.memory = Memory(self)
        self.audition = Audition(self)
        self.typing = Typing(Hands(self))
        self.instruction = Instruction(
            self, self.memory, self.audition, self.language)


class TypeLetterTask:

    def run(self, agent):
        vision = agent.vision
        audition = agent.audition
        typing = agent.typing
        instruction = agent.instruction

        def read_executor(step, context):
            obj = step.obj
            query = Query(x=step.x, y=step.y)
            context.set(obj, vision.find_and_encode(query))
        instruction.set_executor('read', read_executor)

        def type_executor(step, context):
            obj = step.obj
            typing.type(context.get(obj))
        instruction.set_executor('type', type_executor)

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
