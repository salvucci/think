from think import Item, Module, Query


class Language(Module):

    def __init__(self, agent):
        super().__init__('language', agent)
        self.interpreters = []
    
    def add_interpreter(self, interpreter):
        self.interpreters.append(interpreter)
        return self

    def interpret(self, text):
        self.log('interpreting "{}"'.format(text))
        words = text.split(' ')
        if len(words) == 2 and words[0] == 'to':
            return Item(isa='goal', name=words[1])
        else:
            for interpreter in self.interpreters:
                sem = interpreter(words)
                if sem:
                    self.log('interpreted as {}'.format(sem))
                    return sem
            return None
