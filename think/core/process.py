import threading
from .clock import Clock


class Cancel:
    WILL_RUN = 1
    HAS_RUN = 2
    CANCELED = 3

    def __init__(self):
        self.status = Cancel.WILL_RUN
        self.lock = threading.Lock()

    def try_run(self):
        with self.lock:
            if self.status == Cancel.WILL_RUN:
                self.status = Cancel.HAS_RUN
                return True
            else:
                return False

    def try_cancel(self):
        with self.lock:
            if self.status == Cancel.WILL_RUN:
                self.status = Cancel.CANCELED
                return True
            else:
                return False


class Process:

    def __init__(self, name, clock=None):
        self.name = name
        self.clock = clock if clock is not None else Clock()

    def time(self):
        return self.clock.time()

    def run(self, action, delay=0.0):
        def _actions():
            if delay > 0:
                self.wait(delay)
            if action is not None:
                action()
            self.clock.deregister()
        thread = threading.Thread(target=_actions)
        self.clock.register(thread)
        thread.start()
        return thread

    def run_can_cancel(self, action, delay=0.0):
        cancel = Cancel()

        def _actions():
            if delay > 0:
                self.wait(delay)
            if cancel.try_run() and action is not None:
                action()
            self.clock.deregister()
        thread = threading.Thread(target=_actions)
        self.clock.register(thread)
        thread.start()
        return cancel

    def report_event(self):
        self.clock.report_event()

    def wait_for_next_event(self):
        self.clock.wait_for_next_event()

    def wait_until(self, time):
        self.clock.wait_until(time)

    def wait(self, seconds):
        self.wait_until(self.time() + seconds)

    def wait_for_all(self):
        self.clock.wait_for_all()

    def log(self, message, source=None):
        if source is None:
            source = self.name
        self.clock.log(message, source)

    def debug(self, message, source=None):
        if source is None:
            source = self.name
        self.clock.debug(message, source)
