from inspect import signature
from think import Module, Item, Query
from .memory import Chunk


class _InstructionGoal:

    def __init__(self, name):
        self.name = name
        self.steps = []

    def add(self, step):
        self.steps.append(step)


class Instruction(Module):

    def __init__(self, agent, memory, audition, language):
        super().__init__('instruction', agent)
        self.memory = memory
        self.language = language
        self.audition = audition
        self.goals = {}
        self.executors = {}

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
        while sem is not None and sem.isa == 'action':
            step = Chunk(**sem.slots)
            step.set('goal', goal.name).set('previous', previous)
            goal.add(step)
            self.memory.store(step)
            previous = step
            sem = self._next_sem()
        return goal.name

    def set_executor(self, action, fn):
        self.executors[action] = fn

    def execute(self, name, context=None):
        if name not in self.goals:
            raise Exception
        goal = self.goals[name]
        self.log('executing goal {}'.format(goal.name))
        if context is None:
            context = Item()
        previous = 'start'
        for step in goal.steps:
            if step.action in self.executors:
                chunk = self.memory.recall(goal=goal.name, previous=previous)
                self.log('executing step {}'.format(step))
                executor = self.executors[step.action]
                executor(step, context)
            previous = step
        return context
