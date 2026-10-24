import unittest
import numpy as np

from faultscope.phasors import phases,sequences,base_current
class PhasorTests(unittest.TestCase):
    def test_roundtrip(self):np.testing.assert_allclose(sequences(phases([.1j,1-.1j,.2])),[.1j,1-.1j,.2],atol=1e-12)
    def test_base(self):self.assertAlmostEqual(base_current(100,11),5248.63881081478)
