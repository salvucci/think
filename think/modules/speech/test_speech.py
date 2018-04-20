import unittest
from think import Speech, Agent


class SpeechTest(unittest.TestCase):

    def test_speech(self, output=False):
        agent = Agent(output=output)
        speech = Speech(agent)
        speech.say("Hello I am the speech module")
        speech.subvocalize("Goodbye all")
        agent.wait_for_all()
        self.assertAlmostEqual(agent.time(), 3.650, 2)


class SyllableTest(unittest.TestCase):
    TEST_WORDS = {"the": 1, "of": 1, "to": 1,
                  "and": 1, "a": 1, "in": 1, "is": 1, "it": 1, "you": 1, "that": 1, "he": 1,
                  "was": 1, "for": 1, "on": 1, "are": 1, "with": 1, "as": 1, "I": 1, "his": 1,
                  "they": 1, "be": 1, "at": 1, "one": 1, "have": 1, "this": 1, "from": 1,
                  "or": 1, "had": 1, "by": 1, "hot": 1, "word": 1, "but": 1, "what": 1,
                  "some": 1, "we": 1, "can": 1, "out": 1, "other": 2, "were": 1, "all": 1,
                  "there": 1, "when": 1, "up": 1, "use": 1, "your": 1, "how": 1, "said": 1,
                  "an": 1, "each": 1, "she": 1, "which": 1, "do": 1, "their": 1, "time": 1,
                  "if": 1, "will": 1, "way": 1, "about": 2, "many": 2, "then": 1, "them": 1,
                  "write": 1, "would": 1, "like": 1, "so": 1, "these": 1, "her": 1, "long": 1,
                  "make": 1, "thing": 1, "see": 1, "him": 1, "two": 1, "has": 1, "look": 1,
                  "more": 1, "day": 1, "could": 1, "go": 1, "come": 1, "did": 1, "number": 2,
                  "sound": 1, "no": 1, "most": 1, "people": 2, "my": 1, "over": 2, "know": 1,
                  "water": 2, "than": 1, "call": 1, "first": 1, "who": 1, "may": 1, "down": 1,
                  "side": 1, "been": 1, "now": 1, "find": 1, "any": 2, "new": 1, "work": 1,
                  "part": 1, "take": 1, "get": 1, "place": 1, "made": 1, "live": 1, "where": 1,
                  "after": 2, "back": 1, "little": 2, "only": 2, "round": 1, "man": 1, "year": 1,
                  "came": 1, "show": 1, "every": 3, "good": 1, "me": 1, "give": 1, "our": 1,
                  "under": 2, "name": 1, "very": 2, "through": 1, "just": 1, "form": 1,
                  "sentence": 2, "great": 1, "think": 1, "say": 1, "help": 1, "low": 1, "line": 1,
                  "differ": 2, "turn": 1, "cause": 1, "much": 1, "mean": 1, "before": 2,
                  "move": 1, "right": 1, "boy": 1, "old": 1, "too": 1, "same": 1, "tell": 1,
                  "does": 1, "set": 1, "three": 1, "want": 1, "air": 1, "well": 1, "also": 2,
                  "play": 1, "small": 1, "end": 1, "put": 1, "home": 1, "read": 1, "hand": 1,
                  "port": 1, "large": 1, "spell": 1, "add": 1, "even": 2, "land": 1, "here": 1,
                  "must": 1, "big": 1, "high": 1, "such": 1, "follow": 2, "act": 1, "why": 1,
                  "ask": 1, "men": 1, "change": 1, "went": 1, "light": 1, "kind": 1, "off": 1,
                  "need": 1, "house": 1, "picture": 2, "try": 1, "us": 1, "again": 2, "animal": 3,
                  "point": 1, "mother": 2, "world": 1, "near": 1, "build": 1, "self": 1,
                  "earth": 1, "father": 2, "head": 1, "stand": 1, "own": 1, "page": 1,
                  "should": 1, "country": 2, "found": 1, "answer": 2, "school": 1, "grow": 1,
                  "study": 2, "still": 1, "learn": 1, "plant": 1, "cover": 2, "food": 1, "sun": 1,
                  "four": 1, "between": 2, "state": 1, "keep": 1, "eye": 1, "never": 2, "last": 1,
                  "let": 1, "thought": 1, "city": 2, "tree": 1, "cross": 1, "farm": 1, "hard": 1,
                  "start": 1, "might": 1, "story": 2, "saw": 1, "far": 1, "sea": 1, "draw": 1,
                  "left": 1, "late": 1, "run": 1, "don't": 1, "while": 1, "press": 1, "close": 1,
                  "night": 1, "real": 1, "life": 1, "few": 1, "north": 1, "open": 2, "seem": 1,
                  "together": 3, "next": 1, "white": 1, "children": 2, "begin": 2, "got": 1,
                  "walk": 1, "example": 3, "ease": 1, "paper": 2, "group": 1, "always": 2,
                  "music": 2, "those": 1, "both": 1, "mark": 1, "often": 2, "letter": 2,
                  "until": 2, "mile": 1, "river": 2, "car": 1, "feet": 1, "care": 1, "second": 2,
                  "book": 1, "carry": 2, "took": 1, "science": 2, "eat": 1, "room": 1,
                  "friend": 1, "began": 2, "idea": 3, "fish": 1, "mountain": 2, "stop": 1,
                  "once": 1, "base": 1, "hear": 1, "horse": 1, "cut": 1, "sure": 1, "watch": 1,
                  "color": 2, "face": 1, "wood": 1, "main": 1, "enough": 2, "plain": 1, "girl": 1,
                  "usual": 3, "young": 1, "ready": 2, "above": 2, "ever": 2, "red": 1, "list": 1,
                  "though": 1, "feel": 1, "talk": 1, "bird": 1, "soon": 1, "body": 2, "dog": 1,
                  "family": 3, "direct": 2, "pose": 1, "leave": 1, "song": 1, "measure": 2,
                  "door": 1, "product": 2, "black": 1, "short": 1, "numeral": 3, "class": 1,
                  "wind": 1, "question": 2, "happen": 2, "complete": 2, "ship": 1, "area": 3,
                  "half": 1, "rock": 1, "order": 2, "fire": 1, "south": 1, "problem": 2,
                  "piece": 1, "told": 1, "knew": 1, "pass": 1, "since": 1, "top": 1, "whole": 1,
                  "king": 1, "space": 1, "heard": 1, "best": 1, "hour": 1, "better": 2,
                  "true .": 1, "during": 2, "hundred": 2, "five": 1, "remember": 3, "step": 1,
                  "early": 2, "hold": 1, "west": 1, "ground": 1, "interest": 3, "reach": 1,
                  "fast": 1, "verb": 1, "sing": 1, "listen": 2, "six": 1, "table": 2, "travel": 2,
                  "less": 1, "morning": 2, "ten": 1, "simple": 2, "several": 3, "vowel": 2,
                  "toward": 2, "war": 1, "lay": 1, "against": 2, "pattern": 2, "slow": 1,
                  "center": 2, "love": 1, "person": 2, "money": 2, "serve": 1, "appear": 2,
                  "road": 1, "map": 1, "rain": 1, "rule": 1, "govern": 2, "pull": 1, "cold": 1,
                  "notice": 2, "voice": 1, "unit": 2, "power": 2, "town": 1, "fine": 1,
                  "certain": 2, "fly": 1, "fall": 1, "lead": 1, "cry": 1, "dark": 1, "machine": 2,
                  "note": 1, "wait": 1, "plan": 1, "figure": 2, "star": 1, "box": 1, "noun": 1,
                  "field": 1, "rest": 1, "correct": 2, "able": 2, "pound": 1, "done": 1,
                  "beauty": 2, "drive": 1, "stood": 1, "contain": 2, "front": 1, "teach": 1,
                  "week": 1, "final": 2, "gave": 1, "green": 1, "oh": 1, "quick": 1, "develop": 3,
                  "ocean": 2, "warm": 1, "free": 1, "minute": 2, "strong": 1, "special": 2,
                  "mind": 1, "behind": 2, "clear": 1, "tail": 1, "produce": 2, "fact": 1,
                  "street": 1, "inch": 1, "multiply": 3, "nothing": 2, "course": 1, "stay": 1,
                  "wheel": 1, "full": 1, "force": 1, "blue": 1, "object": 2, "decide": 2,
                  "surface": 2, "deep": 1, "moon": 1, "island": 2, "foot": 1, "system": 2,
                  "busy": 2, "test": 1, "record": 2, "boat": 1, "common": 2, "gold": 1,
                  "possible": 3, "plane": 1, "stead": 1, "dry": 1, "wonder": 2, "laugh": 1,
                  "thousand": 2, "ago": 2, "ran": 1, "check": 1, "game": 1, "shape": 1,
                  "equate": 2, "miss": 1, "brought": 1, "heat": 1, "snow": 1, "tire": 1,
                  "bring": 1, "yes": 1, "distant": 2, "fill": 1, "east": 1, "paint": 1,
                  "language": 2, "among": 2}

    def test_syllable_count(self):
        agent = Agent()
        speech = Speech(agent)
        errors = 0
        for word, syll in SyllableTest.TEST_WORDS.items():
            count = speech.count_syllables(word)
            if syll != count:
                errors += 1
        self.assertEqual(errors, 0)
