import logging
import threading
import time

from .logger import get_think_logger

_DEBUG = False


try:

    import os
    os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'
    import pygame

    def sleep(sec):
        pygame.time.delay(int(1000 * sec))

except ImportError as e:

    def sleep(sec):
        time.sleep(sec)


class _ThreadInfo:
    RUNNING = 1
    TIMED_WAIT = 2
    EVENT_WAIT = 3
    NEXT = 4
    DONE = 5

    def __init__(self, index):
        self.index = index
        self.parent = threading.current_thread()
        self.status = _ThreadInfo.RUNNING
        self.requested_time = None
        self.last_think_time = -.001

    status_labels = {1: 'running', 2: 'timed_wait',
                     3: 'event_wait', 4: 'next', 5: 'done'}

    def __str__(self):
        return '{}: {} [{}, {}]'.format(self.index, _ThreadInfo.status_labels[self.status],
                                        self.requested_time, self.last_think_time)


class Clock:

    def __init__(self, real_time=False, output=True):
        self._time = 0.0
        self.time_lock = threading.Lock()
        self.real_time = real_time
        self.threads = {}
        self.threads_lock = threading.Lock()
        self.event_flag = False
        self.barrier = threading.Barrier(0, lambda: self.update_all())
        self.barrier_lock = threading.Lock()
        self.set_output(output)

    def set_output(self, output):
        if isinstance(output, logging.Logger):
            self.logger = output
        elif output:
            self.logger = get_think_logger()
        else:
            self.logger = None

    def advance(self, dt):
        with self.time_lock:
            self._time += dt
            if self.real_time:
                sleep(dt)

    def time(self):
        with self.time_lock:
            return self._time

    def set(self, t):
        with self.time_lock:
            old_time = self._time
            self._time = t
            if self.real_time and old_time < t:
                sleep(t - old_time)

    def register(self, thread):
        n_threads = 0
        with self.threads_lock:
            self.threads[thread] = _ThreadInfo(len(self.threads) + 1)
            if _DEBUG:
                self.debug('register thread: ' + thread.name)
            n_threads = len(self.threads)
        with self.barrier_lock:
            self.barrier._parties = n_threads  # self.barrier._parties + 1
            if _DEBUG:
                self.debug('({} threads in barrier)'.format(
                    self.barrier.parties))

    def n_threads(self):
        with self.threads_lock:
            return len(self.threads)

    def n_children(self, parent=None):
        if parent is None:
            parent = threading.current_thread()
        with self.threads_lock:
            count = 0
            for info in self.threads.values():
                if info.parent == parent:
                    count += 1
            return count

    def thread_index(self, thread=None):
        if thread is None:
            thread = threading.current_thread()
        with self.threads_lock:
            return self.threads[thread].index

    def deregister(self):
        with self.threads_lock:
            self.threads[threading.current_thread()].status = _ThreadInfo.DONE
        self.barrier.wait()

    def report_think(self):
        with self.threads_lock:
            self.threads[threading.current_thread(
            )].last_think_time = self.time()
        if _DEBUG:
            self.debug('reported think')

    def report_event(self):
        self.event_flag = True
        if _DEBUG:
            self.debug('reported event')

    def wait_for_next_event(self):
        with self.threads_lock:
            info = self.threads[threading.current_thread()]
            info.status = _ThreadInfo.EVENT_WAIT
        self._wait_my_turn()

    def wait_until(self, time):
        with self.threads_lock:
            info = self.threads[threading.current_thread()]
            info.status = _ThreadInfo.TIMED_WAIT
            info.requested_time = time
        self._wait_my_turn()

    def _wait_my_turn(self):
        if _DEBUG:
            self.debug('waiting at barrier...')
        self.barrier.wait()
        while not self._is_running(threading.current_thread()):
            self.barrier.wait()

    def _is_running(self, thread):
        with self.threads_lock:
            return self.threads[thread].status == _ThreadInfo.RUNNING

    def _debug_threads(self):
        for thread, info in self.threads.items():
            self.debug('[{}] -> {}'.format(thread.name, info))

    def update_all(self):
        with self.threads_lock:
            if _DEBUG:
                self.debug('updating: event_flag = {}'.format(self.event_flag))
                self.debug('-----')
                self._debug_threads()

            dones = []
            for thread, info in self.threads.items():
                if info.status == _ThreadInfo.DONE:
                    dones.append(thread)
            for thread in dones:
                del self.threads[thread]
                if _DEBUG:
                    self.debug('deleting thread [{}]'.format(thread.name))
                with self.barrier_lock:
                    self.barrier._parties = self.barrier._parties - 1

            if (self.event_flag):
                self.event_flag = False
                self._change_status_locked(
                    _ThreadInfo.EVENT_WAIT, _ThreadInfo.NEXT)
            count = self._run_next_threads_locked()
            if count == 0:
                self._run_timed_threads_locked()
            if _DEBUG:
                self.debug('--> [t={}]'.format(self.time()))
                self._debug_threads()
                self.debug('-----')

    def _change_status_locked(self, old, new):
        count = 0
        for info in self.threads.values():
            if info.status == old:
                info.status = new
                count += 1
        return count

    def _run_next_threads_locked(self):
        min_time = None
        for info in self.threads.values():
            if info.status == _ThreadInfo.NEXT:
                time = info.last_think_time
                if min_time is None or time < min_time:
                    min_time = time
        if min_time is not None:
            count = 0
            for info in self.threads.values():
                if info.status == _ThreadInfo.NEXT and info.last_think_time <= min_time:
                    info.status = _ThreadInfo.RUNNING
                    count += 1
            return count
        else:
            return 0

    def _run_timed_threads_locked(self):
        min_time = None
        for info in self.threads.values():
            if info.status == _ThreadInfo.TIMED_WAIT:
                time = info.requested_time
                if min_time is None or time < min_time:
                    min_time = time
        if min_time is not None:
            count = 0
            for info in self.threads.values():
                if info.status == _ThreadInfo.TIMED_WAIT and info.requested_time <= min_time:
                    info.status = _ThreadInfo.RUNNING
                    info.requested_time = None
                    count += 1
            self.set(min_time)
            return count
        else:
            return 0

    def wait_for_all(self):
        self.barrier.wait()
        while len(self.threads) > 1:
            if _DEBUG:
                self.debug('waiting for all...')
            self.barrier.wait()

    def log(self, message, source='clock'):
        if self.logger:
            self.logger.info(
                message, extra={'time': self.time(), 'source': source})

    def debug(self, message, source='clock'):
        if _DEBUG and self.logger:
            message = '[{}] {}'.format(
                threading.current_thread().name, message)
            self.logger.debug(
                message, extra={'time': self.time(), 'source': source})
