try:

    import os
    os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'
    import pygame

    from .item import Area

    class DisplayIcon:

        def __init__(self, size):
            self.visual = None
            self.surface = pygame.Surface(size, pygame.SRCALPHA)
            self.surface.fill((255, 255, 255, 0))

        def draw(self, screen, center=True):
            if self.visual:
                sw, sh = self.surface.get_size() if center else (0, 0)
                screen.blit(self.surface,
                            (self.visual.x + (self.visual.w // 2) - (sw // 2),
                             self.visual.y + (self.visual.h // 2) - (sh // 2)))

    class AttendIcon(DisplayIcon):

        def __init__(self):
            super().__init__((30, 30))
            pygame.draw.circle(self.surface,
                               (255, 255, 0, 128), (15, 15), 15)

    class PointerIcon(DisplayIcon):

        def __init__(self):
            super().__init__((18, 17))

            def draw_pointer(x, y, color):
                pygame.draw.polygon(self.surface, color,
                                    [(x, y), (x + 10, y + 10), (x + 5, y + 9), (x + 8, y + 15),
                                     (x + 6, y + 16), (x + 3, y + 10), (x, y + 14)])

            draw_pointer(0, 0, (255, 255, 255))
            draw_pointer(2, 0, (255, 255, 255))
            draw_pointer(1, 0, (0, 0, 255))

    class ClickIcon(DisplayIcon):

        def __init__(self):
            super().__init__((30, 30))

            def draw_line(sx, sy):
                pygame.draw.line(self.surface, (0, 0, 255),
                                 (15 + 5*sx, 15 + 5*sy), (15 + 15*sx, 15 + 15*sy))

            for sx in [-1, +1]:
                for sy in [-1, +1]:
                    draw_line(sx, sy)

    class DisplayWindow:

        def __init__(self, display, size=(500, 500)):
            self.display = display
            pygame.init()
            self.screen = pygame.display.set_mode(size)
            self.font = pygame.font.Font('freesansbold.ttf', 16)
            self.attend = AttendIcon()
            self.pointer = PointerIcon()
            self.click = ClickIcon()

        def set_attend(self, visual):
            self.attend.visual = visual
            self.draw()

        def set_pointer(self, visual):
            self.pointer.visual = visual
            self.click.visual = None
            self.draw()

        def set_click(self, visual):
            self.click.visual = visual
            self.draw()

        def draw(self):
            self.screen.fill((255, 255, 255))

            for v in self.display.visuals:
                if v.isa == 'text' or v.isa == 'letter' or v.isa == 'button':
                    self.draw_text(v)
                    if v.isa == 'button':
                        self.draw_rect(v, dw=20, dh=20, color=(16, 16, 16))
                else:
                    self.draw_rect(v, stroke=3)

            self.pointer.draw(self.screen, center=False)
            self.click.draw(self.screen)
            self.attend.draw(self.screen)

            pygame.display.update()

        def draw_rect(self, visual, dw=0, dh=0, color=(0, 0, 0), stroke=1):
            pygame.draw.rect(self.screen, color,
                             (visual.x - (dw // 2), visual.y - (dh // 2),
                              visual.w + dw, visual.h + dh),
                             stroke)

        def draw_circle(self, visual, dr=0, color=(0, 0, 0), stroke=1):
            pygame.draw.circle(self.screen, color,
                               (visual.x + (visual.w // 2),
                                visual.y + (visual.h // 2)),
                               max(visual.w, visual.h) + dr,
                               stroke)

        def draw_text(self, visual, text=None):
            text = text or str(visual.obj)
            surface = self.font.render(text, True, (0, 0, 0))
            rect = surface.get_rect()
            rect.center = (visual.x + (visual.w // 2),
                           visual.y + (visual.h // 2))
            self.screen.blit(surface, rect)


except ImportError as e:

    class DisplayWindow:

        def __init__(self, size=(500, 500)):
            raise Exception('pygame must be installed to draw display window')
