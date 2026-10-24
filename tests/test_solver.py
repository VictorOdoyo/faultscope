import unittest
import numpy as np

from faultscope.solver import analyze
class SolverTests(unittest.TestCase):
    def sample(self,ground=True):return {'base_mva':100,'buses':[{'id':'a','base_kv':11}],'sources':[{'id':'s','bus':'a','z1':[0,.1],'z2':[0,.1],'z0':[0,.1] if ground else None}]}
    def test_three_phase_level(self):
        r=analyze(self.sample());self.assertAlmostEqual(r['fault']['max_phase_rms_a'],52486.3881081478,places=6)
    def test_floating_slg_shifts_voltage_without_current(self):
        r=analyze(self.sample(False),fault_type='slg');self.assertLess(r['fault']['max_phase_rms_a'],1e-8);self.assertLess(r['buses'][0]['phase_voltage_v'][0]['magnitude'],1e-8);self.assertTrue(r['thevenin']['zero_sequence_floating'])
    def test_unsourced_island_rejected(self):
        with self.assertRaises(ValueError):analyze({'buses':[{'id':'a'}]})
