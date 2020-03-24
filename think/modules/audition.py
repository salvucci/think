import math
import random

from think import Buffer, Item, Location, Module, Query

from .utilities import count_syllables, text_to_words


class Aural(Item):

    def __init__(self, isa='aural'):
        super().__init__(isa=isa)
        self.set('heard', False)


class Audition(Module):

    def __init__(self, agent):
        super().__init__("audition", agent)
        self.aurals = []
        self.listen_buffer = Buffer("audition.listen", self)
        self.encode_buffer = Buffer("audition.encode", self)
        self.listen_for_query = None
        self.last_encode_cancel = None
        self.attend_fns = []
        self.encode_fns = []

        self.listen_time = .000
        self.encode_time = .300

        self.syllable_rate = .150

    def add(self, aural, obj):
        self.aurals.append((aural, obj))
        if self.listen_for_query is not None and self.listen_for_query.matches(aural):
            self._finish_listen(aural)
        return self

    def add_speech(self, text):
        def thread():
            for word in text_to_words(text):
                syll = count_syllables(word)
                self.add(Aural('word'), word)
                self.agent.wait(syll * self.syllable_rate)
        self.agent.run_thread(thread)
        return self

    def remove(self, aural):
        new_aurals = []
        for (aur, obj) in self.aurals:
            if aur != aural:
                new_aurals.append((aur, obj))
        self.aurals = new_aurals
        return self

    def clear(self):
        self.aurals = []
        return self

    def add_attend_fn(self, fn):
        self.attend_fns.append(fn)
        return self

    def add_encode_fn(self, fn):
        self.encode_fns.append(fn)
        return self

    def _try_listen(self, query):
        for (aural, obj) in self.aurals:
            if query is not None and query.matches(aural):
                return aural
        return None

    def _construct_query(self, query, heard, kwargs):
        if query is None:
            query = Query(**kwargs)
        if heard is not None and not query.has('heard'):
            query = query.eq('heard', heard)
        return query

    def start_listen(self, query=None, heard=False, **kwargs):
        query = self._construct_query(query, heard, kwargs)
        self.listen_buffer.acquire()
        self.think("listen {}".format(query))
        match = self._try_listen(query)
        if match is not None:
            self._finish_listen(match)
        else:
            duration = self.listen_time
            self.listen_buffer.clear(duration, "listen failed")

    def get_found(self):
        return self.listen_buffer.get_and_release()

    def listen(self, query=None, heard=False, **kwargs):
        query = self._construct_query(query, heard, kwargs)
        self.start_listen(query)
        return self.get_found()

    def start_listen_for(self, query=None, heard=False, **kwargs):
        query = self._construct_query(query, heard, kwargs)
        self.listen_buffer.acquire()
        self.think("wait for {}".format(query))
        aural = self._try_listen(query)
        if aural is not None:
            self._finish_listen(aural)
        else:
            self.listen_for_query = query

    def _finish_listen(self, aural):
        self.listen_for_query = None
        duration = self.listen_time

        def fn():
            aural.set('heard', True)
            for fn in self.attend_fns:
                fn(aural)
        self.listen_buffer.set(aural, duration, "found {}".format(aural), fn)

    def listen_for(self, query=None, heard=False, **kwargs):
        query = self._construct_query(query, heard, kwargs)
        self.start_listen_for(query)
        return self.get_found()

    def start_encode_thread(self, aural, obj, duration):
        if self.last_encode_cancel is not None:
            self.last_encode_cancel.try_cancel()

        def fn():
            self.log('encoded "{}"'.format(obj))
            self.encode_buffer.set(obj)
            aural.set('heard', True)
            self.remove(aural)
            for fn in self.encode_fns:
                fn(aural, object)

        self.last_encode_cancel = self.run_thread_can_cancel(fn, duration)

    def start_encode(self, aural, suppress_think=False):
        self.encode_buffer.acquire()
        if not suppress_think:
            self.think("encode {}".format(aural))
        obj = None
        for (a, o) in self.aurals:
            if a == aural:
                obj = o
        duration = self.encode_time
        if obj is not None:
            self.start_encode_thread(aural, obj, duration)
        else:
            self.encode_buffer.clear(duration, "encode failed")

    def get_encoded(self):
        return self.encode_buffer.get_and_release()

    def encode(self, aural):
        self.start_encode(aural)
        return self.get_encoded()

    def listen_and_encode(self, query=None, heard=False, **kwargs):
        query = self._construct_query(query, heard, kwargs)
        aural = self.listen(query)
        return self.encode(aural) if aural is not None else None

    def listen_for_and_encode(self, query=None, heard=False, **kwargs):
        query = self._construct_query(query, heard, kwargs)
        aural = self.listen_for(query)
        return self.encode(aural) if aural is not None else None
