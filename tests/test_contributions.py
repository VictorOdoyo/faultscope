import unittest
import numpy as np

from faultscope.phasors import phases
class ContributionConventions(unittest.TestCase):
    def test_residual_equals_three_zero_sequence(self):
        seq=np.array([.2-.3j,.7j,.1]);self.assertLess(abs(sum(phases(seq))-3*seq[0]),1e-12)
