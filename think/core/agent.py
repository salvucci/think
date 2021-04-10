"""
This module provides the basic agent functionality.
"""

import threading

from .clock import Clock
from .process import Process

_DEBUG = False


class Agent(Process):
    """Represents a cognitive agent
    """

    def __init__(self, name='agent', clock=None, output=False):
        """Creates an agent

        Args:
            name (str, optional): [description]. Defaults to 'agent'.
            clock ([type], optional): [description]. Defaults to None.
            output (bool, optional): [description]. Defaults to False.
        """
        super().__init__(name, clock or Clock(output=output))
        self.think_time = .050
        self.clock.register(threading.current_thread())
        self.think_worker = Worker('think', self)
        self.modules = {}

    def indexed_name(self):
        """Provides the name of the agent including its thread index

        Returns:
            str: agent name with thread index
        """
        name = self.name
        if self.clock.n_children() > 1:
            name += '[{}]'.format(self.clock.thread_index())
        return name

    def add_module(self, module):
        """Adds a module to the agent

        Args:
            module (Module): module to add
        """
        self.modules[module.name] = module

    def module(self, name):
        """Returns the named module

        Args:
            name (string): name of the module

        Returns:
            Module: the module
        """
        return self.modules[name]

    def think(self, message):
        self.think_worker.acquire()
        self.clock.report_think()
        self.log(message)
        self.wait_until(self.time() + self.think_time)
        self.think_worker.release()
        self.report_event()
        self.wait_for_next_event()


class Module(Process):

    def __init__(self, name, agent):
        super().__init__(name, agent.clock)
        self.agent = agent
        agent.add_module(self)

    def think(self, message):
        self.agent.think(message)

    def log(self, message):
        super().log(message, self.agent.name + '.' + self.name)

    def debug(self, message):
        super().debug(message, self.agent.name + '.' + self.name)


class Worker:

    def __init__(self, name, process):
        self.name = name
        self.process = process
        self.lock = threading.Lock()

    def acquire(self):
        locked = self.lock.acquire(False)
        while not locked:
            if _DEBUG:
                self.process.debug(
                    'worker "{}" acquire failed'.format(self.name))
            self.process.wait_for_next_event()
            locked = self.lock.acquire(False)
        if _DEBUG:
            self.process.debug('worker "{}" acquired'.format(self.name))

    def run(self, delay=0.0, message=None, action=None, release=True):
        def _actions():
            if message is not None:
                self.process.log(message)
            if action is not None:
                action()
            if release:
                self.release()
        self.process.run_thread(_actions, delay)

    def wait_until_free(self):
        locked = self.lock.acquire(False)
        while not locked:
            self.process.wait_for_next_event()
            locked = self.lock.acquire(False)
        self.lock.release()

    def release(self):
        self.lock.release()
        self.process.report_event()
        self.process.wait_for_next_event()
        if _DEBUG:
            self.process.debug('worker "{}" released'.format(self.name))


class Buffer(Worker):

    def __init__(self, name, module):
        super().__init__(name, module)
        self.content_worker = Worker(name + '_content', module)
        self.contents = None

    def acquire(self):
        super().acquire()
        self.content_worker.acquire()
        if _DEBUG:
            self.process.debug('buffer "{}" acquired'.format(self.name))

    def set(self, contents, delay=None, message=None, action=None):
        if delay is None:
            self.contents = contents
            self.content_worker.release()
        else:
            def _action():
                self.contents = contents
                self.content_worker.release()
                if action is not None:
                    action()
            self.content_worker.run(delay, message, _action, False)

    def clear(self, delay=None, message=None, action=None):
        self.set(None, delay, message, action)

    def wait_for_content(self):
        if _DEBUG:
            self.process.debug(
                'buffer "{}" waiting for content'.format(self.name))
        self.content_worker.acquire()
        self.content_worker.release()

    def get_and_release(self):
        self.wait_for_content()
        result = self.contents
        if _DEBUG:
            self.process.debug('buffer "{}" released'.format(self.name))
        super().release()
        return result
