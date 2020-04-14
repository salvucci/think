from inspect import signature

from think import Module, Query

from .memory import Chunk


class _InstructionGoal:

    def __init__(self, name):
        self.name = name
        self.actions = []

    def add(self, action):
        self.actions.append(action)


class Instruction(Module):

    def __init__(self, agent, memory, audition, language):
        super().__init__('instruction', agent)
        self.memory = memory
        self.language = language
        self.audition = audition
        self.goals = {}
        self.executors = []

    def _next_sem(self):
        text = self.audition.listen_for_and_encode()
        return self.language.interpret(text)

    def listen_and_learn(self):
        self.log('listening for instructions')
        sem = self._next_sem()
        if sem.isa != 'goal':
            return None
        goal = _InstructionGoal(sem.name)
        self.goals[goal.name] = goal
        previous = 'start'
        sem = self._next_sem()
        while sem is not None and sem.isa != 'done':
            action = Chunk(**sem.slots)
            action.set('goal', goal.name).set('previous', previous)
            goal.add(action)
            self.memory.store(action, boost=10)
            previous = action
            sem = self._next_sem()
        return goal.name

    def add_executor(self, executor):
        self.executors.append(executor)
        return self

    def execute(self, name, context=None):
        if name not in self.goals:
            raise Exception
        goal = self.goals[name]
        self.log('executing goal {}'.format(goal.name))
        context = context or Chunk()
        previous = 'start'
        for action in goal.actions:
            self.memory.recall(goal=goal.name, previous=previous)
            self.log('executing action {}'.format(action))
            for executor in self.executors:
                executed = executor(action, context)
                if executed:
                    break
            previous = action
        return context
