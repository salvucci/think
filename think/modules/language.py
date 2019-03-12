from think import Module, Query, Item


class Language(Module):

    def __init__(self, agent, vision):
        super().__init__('instruction', agent)
        self.vision = vision

    def interpret(self, text):
        words = text.split(' ')
        if len(words) == 2 and words[0] == 'to':
            return Item(isa='goal', name=words[1])
        elif words[0] == 'read':
            sem = Item(isa='action', action='read', object=words[1])
            pointer = self.vision.find(isa='pointer')
            if pointer is not None:
                self.vision.encode(pointer)
                sem.set('x', pointer.x).set('y', pointer.y)
            return sem
        elif words[0] == 'done':
            return Item(isa='done')
        else:
            return Item(isa='action', action=words[0], object=words[1])
