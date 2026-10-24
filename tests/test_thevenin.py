import unittest
import numpy as np

from faultscope.thevenin import driving_point
class TheveninTests(unittest.TestCase):
    def test_floating_component(self):
        y=np.array([[-5j,5j],[5j,-5j]]);r=driving_point(y,1,True)
        self.assertTrue(r['floating']);np.testing.assert_allclose(r['mode'],[1,1])
    def test_series_source(self):
        y=np.array([[-15j,5j],[5j,-5j]]);r=driving_point(y,1)
        self.assertAlmostEqual(r['z'].imag,.3)
