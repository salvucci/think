import unittest
from think import Agent, Memory, Speech, Arithmetic


class ArithmeticTest(unittest.TestCase):

    def test_arithmetic(self):
        agent = Agent(output=False)
        arithmetic = Arithmetic(agent, Memory(agent), Speech(agent))
        arithmetic.count_to(5)

        self.assertEqual(0, arithmetic.add(0, 0))
        self.assertEqual(5, arithmetic.add(2, 3))
        self.assertEqual(17, arithmetic.add(8, 9))

        self.assertEqual(0, arithmetic.multiply(0, 0))
        self.assertEqual(0, arithmetic.multiply(7, 0))
        self.assertEqual(12, arithmetic.multiply(3, 4))
        self.assertEqual(121, arithmetic.multiply(11, 11))


class NumbersTest(unittest.TestCase):
    TEST_PAIRS = [(0, "zero"), (1, "one"), (-4, "negative four"),
                  (53, "fifty-three"),
                  (129, "one hundred twenty-nine"),
                  (2463, "two thousand four hundred sixty-three"),
                  (7000008, "seven million eight")]

    def test_num_to_text(self):
        agent = Agent()
        arithmetic = Arithmetic(agent, Memory(agent), Speech(agent))
        errors = 0
        for pair in NumbersTest.TEST_PAIRS:
            if arithmetic.num_to_text(pair[0]) != pair[1]:
                errors += 1
        self.assertEqual(errors, 0)
