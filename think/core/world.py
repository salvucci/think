import threading

from .clock import Clock
from .process import Process


class Task(Process):

    def __init__(self, name='task', clock=None):
        super().__init__(name, clock)
        self.events = []

    def record(self, event):
        self.events.append((self.time(), event))
        return self


class World:

    def __init__(self, *processes):
        self.processes = processes
        clocks = [p.clock for p in self.processes if p.clock is not None]
        clock = clocks[0] if len(clocks) > 0 else Clock()
        for p in self.processes:
            p.clock = clock
        clock.register(threading.current_thread())

    def run(self, time, output=None, real_time=None):
        if len(self.processes) > 0:
            p0 = self.processes[0]
            if output is not None:
                p0.clock.set_output(output)
            if real_time is not None:
                p0.clock.real_time = real_time
            for p in self.processes[1:]:
                p0.run_thread(lambda: p.run(time=time))
            p0.run(time=time)
            p0.wait_for_all()
