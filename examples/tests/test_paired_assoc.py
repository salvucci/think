import unittest

from examples.paired_assoc import PairedAssociatesSimulation


class PairedAssociatesTest(unittest.TestCase):

    def test_paired_associates(self, output=False):
        sim = PairedAssociatesSimulation(n_sims=3)
        result_correct, result_rt = sim.run()
        self.assertGreater(result_correct.r, .80)
        self.assertGreater(result_rt.r, .80)
        self.assertLess(result_correct.nrmse, .20)
        self.assertLess(result_rt.nrmse, .20)
