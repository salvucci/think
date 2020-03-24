from think import Module, Worker


class Hands(Module):
    ON_KEYBOARD = 1
    ON_MOUSE = 2

    def __init__(self, agent, pos=None):
        super().__init__("hands", agent)
        self.pos = pos or Hands.ON_KEYBOARD
        self.worker = Worker("hands", self)

    def on_mouse(self):
        return self.pos == Hands.ON_MOUSE

    def on_keyboard(self):
        return self.pos == Hands.ON_KEYBOARD

    def move(self, pos):
        self.pos = pos
        return self
