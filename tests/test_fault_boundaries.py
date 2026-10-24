import unittest
import numpy as np

from faultscope.boundaries import sequence_fault
class FaultBoundaryTests(unittest.TestCase):
    def test_slg_three_equal_networks(self):
        i=sequence_fault('slg',1,.1j,.1j,.1j,0j);np.testing.assert_allclose(i,[-10j/3]*3)
    def test_open_ground_has_no_slg_current(self):np.testing.assert_allclose(sequence_fault('slg',1,.1j,.1j,None,0j),0)
    def test_ll_positive_negative_cancel(self):
        i0,i1,i2=sequence_fault('ll',1,.1j,.1j,.1j,0j);self.assertEqual(i0,0);self.assertAlmostEqual(abs(i1+i2),0)
