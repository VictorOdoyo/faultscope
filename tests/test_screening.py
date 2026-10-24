import unittest
import numpy as np

from faultscope.screening import peak_factor
class ScreeningTests(unittest.TestCase):
    def test_limits(self):self.assertAlmostEqual(peak_factor(0,1),2);self.assertAlmostEqual(peak_factor(1,0),1.02)
    def test_monotonic_rx(self):self.assertGreater(peak_factor(.1,1),peak_factor(1,1))
