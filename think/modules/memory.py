import math
import random
from think import Module, Buffer, Item, Query


class Chunk(Item):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.id = self.get('id') or self.get(
            'name') or self.get('isa') or 'chunk'
        self.creation_time = None
        self.activation = -math.log(.100)
        self.transient_activation = None
        self.use_count = 0
        self.uses = []

    def increment_use(self):
        self.use_count += 1

    def add_use(self, time):
        self.uses.append(time)

    def __str__(self):
        return "<{}>{}".format(self.id, self.slots)


class Memory(Module):

    NO_DECAY = 1
    OPTIMIZED_DECAY = 2
    ADVANCED_DECAY = 3

    def __init__(self, agent, decay=None):
        super().__init__("memory", agent)
        self.decay = decay or Memory.NO_DECAY
        self.chunks = {}
        self.buffer = Buffer("memory", self)
        self.decay_rate = 0.5
        self.retrieval_threshold = 0.0
        self.latency_factor = 1.0
        self.activation_noise = None
        self._unique = 1

    def _uniquify(self, id):
        if id in self.chunks:
            self._unique += 1
            return self._uniquify("{}~{}".format(id, self._unique))
        else:
            return id

    def add(self, chunk=None, **kwargs):
        if not chunk:
            chunk = Chunk(**kwargs)
        chunk.id = self._uniquify(chunk.id)
        self.chunks[chunk.id] = chunk
        return chunk

    def get(self, id):
        return self.chunks[id]

    def _add_use(self, chunk):
        if self.decay == Memory.OPTIMIZED_DECAY:
            chunk.increment_use()
        elif self.decay == Memory.ADVANCED_DECAY:
            chunk.add_use(self.time())

    def _get_match(self, chunk):
        for existing in self.chunks.values():
            if existing.equals(chunk):
                return existing
        return None

    def store(self, chunk=None, **kwargs):
        if not chunk:
            chunk = Chunk(**kwargs)
        self.think("store {}".format(chunk))
        match = self._get_match(chunk)
        if match is not None:
            self.log("stored and merged into {}".format(match))
            self._add_use(match)
            chunk = match
        else:
            self.log("stored {}".format(chunk))
            chunk.id = self._uniquify(chunk.id)
            chunk.creation_time = self.time()
            self._add_use(chunk)
            self.add(chunk)
        self._compute_activation(chunk)
        return chunk

    def _compute_activation(self, chunk):
        if self.decay == Memory.NO_DECAY:
            return chunk.activation
        else:
            time = self.time()
            if time <= chunk.creation_time:
                time = chunk.creation_time + .001
            base_level = 0
            if self.decay == Memory.OPTIMIZED_DECAY:
                base_level = (math.log(chunk.use_count / (1 - self.decay_rate))
                              - self.decay_rate * math.log(time - chunk.creation_time))
            elif self.decay == Memory.ADVANCED_DECAY:
                uses = 0
                for use in chunk.uses:
                    uses += math.pow(time - use, -self.decay_rate)
                base_level = math.log(uses)
            chunk.activation = base_level
            return chunk.activation

    def _compute_transient_act(self, chunk):
        act = self._compute_activation(chunk)
        if self.activation_noise is not None:
            act += random.gauss(0, self.activation_noise)
        chunk.transient_activation = act
        return chunk.transient_activation

    def compute_prob_recall(self, chunk):
        if self.activation_noise is not None:
            act = self._compute_activation(chunk)
            exp = -(act - self.retrieval_threshold) / self.activation_noise
            return 1 / (1 + math.exp(exp))
        else:
            return None

    def compute_recall_time(self, chunk):
        return self.latency_factor * math.exp(min(-chunk.activation, self.retrieval_threshold))

    def _get_chunk(self, query):
        matches = []
        for chunk in self.chunks.values():
            if query.matches(chunk):
                matches.append(chunk)
        best_chunk = None
        best_act = self.retrieval_threshold
        for chunk in matches:
            act = self._compute_transient_act(chunk)
            if act > best_act:
                best_chunk = chunk
                best_act = act
        return best_chunk

    def start_recall(self, query=None, **kwargs):
        if not query or not isinstance(query, Query):
            query = Query(**kwargs)
        self.buffer.acquire()
        self.think("recall {}".format(query))
        self.log("recalling {}".format(query))
        chunk = self._get_chunk(query)
        self._start_recall(chunk)

    def start_recall_by_id(self, id):
        self.buffer.acquire()
        self.think("recall <{}>".format(id))
        self.log("recalling <{}>".format(id))
        chunk = self.get(id)
        act = self._compute_transient_act(chunk)
        self._start_recall(chunk if act >= self.retrieval_threshold else None)

    def _start_recall(self, chunk):
        if chunk is not None:
            duration = self.latency_factor * \
                math.exp(-chunk.transient_activation)
            self.buffer.set(chunk, duration, "recalled {}".format(
                chunk), lambda: self._add_use(chunk))
        else:
            duration = self.latency_factor * \
                math.exp(-self.retrieval_threshold)
            self.buffer.clear(duration, "recall failed")

    def get_recalled(self):
        return self.buffer.get_and_release()

    def recall(self, query=None, **kwargs):
        if not query or not isinstance(query, Query):
            query = Query(**kwargs)
        self.start_recall(query)
        return self.get_recalled()

    def recall_by_id(self, id):
        self.start_recall_by_id(id)
        return self.get_recalled()

    def rehearse(self, chunk):
        self.recall_by_id(chunk.id)

    def clear(self):
        self.chunks = {}
