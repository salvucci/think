import re
from think import Module, Worker


class Speech(Module):

    def __init__(self, agent):
        super().__init__("speech", agent)
        self.worker = Worker("speech", self)
        self.say_fns = []
        self.base_time = .200
        self.syllable_rate = .150

    def add_say_fn(self, fn):
        self.say_fns.append(fn)

    def count_syllables(self, text):
        text = text.strip().lower()
        count = 0
        for word in text.split():
            word = re.sub(r"^([^aeiouy]*)e$", "$1 ee", word)
            word = re.sub(r"([^aeiouy])le$", "$1 ul", word)
            word = re.sub(r"be$", " bee", word)
            word = re.sub(r"es?$", "", word)
            word = re.sub(r"ing$", " ing", word)
            word = re.sub(r"([aeiouy][^aeiouy])ed$", "$1d", word)
            word = re.sub(r"([^cs])ia", "$1i a", word)
            word = re.sub(r"([^s])ea$", "$1e a", word)
            word = re.sub(r"qu", "q", word)
            word = re.sub(r"ienc", "i enc", word)
            word = re.sub(r"ue", "u e", word)
            word = re.sub(r"ual", "u al", word)
            count += len(re.findall(r"[aeiouy]+", word))
        return count

    def calculate_duration(self, word):
        return self.base_time + self.syllable_rate * self.count_syllables(word)

    def _say_word(self, word, s1, s2, s3):
        self.worker.acquire()
        self.think(s1 + ' "' + word + '"')
        self.log(s2 + ' "' + word + '"')
        duration = self.calculate_duration(word)

        def fn():
            for fn in self.say_fns:
                fn(word)
        self.worker.run(duration, s3 + ' "' + word + '"', fn)

    def say(self, text):
        text = re.sub(r"[^A-Za-z\s]", "", str(text))
        for word in text.split():
            self._say_word(word, "say", "saying", "said")

    def subvocalize(self, text):
        text = re.sub(r"[^A-Za-z\s]", "", str(text))
        for word in text.split():
            self._say_word(word, "subvocalize",
                           "subvocalizing", "subvocalized")

    _num_text = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight",
        "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen",
        "seventeen", "eighteen", "nineteen"]
    _num_tens = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy",
                "eighty", "ninety"]

    def _num_to_text(self, n, divisor, unit):
        txt = self.num_to_text(n // divisor) + " " + unit
        rem = n % divisor
        return txt if rem==0 else txt + " " + self.num_to_text(rem)

    def num_to_text(self, n):
        if n < 0:
            return "negative " + self.num_to_text(-n)
        elif n < 20:
            return self._num_text[n]
        elif n < 100:
            txt = self._num_tens[n // 10]
            rem = n % 10
            return txt if rem==0 else txt + "-" + self.num_to_text(rem)
        elif n < 1000:
            return self._num_to_text(n, 100, "hundred")
        elif n < 1000000:
            return self._num_to_text(n, 1000, "thousand")
        elif n < 1000000000:
            return self._num_to_text(n, 1000000, "million")
        elif n < 1000000000000:
            return self._num_to_text(n, 1000000000, "billion")
