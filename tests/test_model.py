import unittest
import numpy as np

from faultscope.model import validate,impedance
class ModelTests(unittest.TestCase):
    def test_zero_impedance_rejected(self):
        with self.assertRaises(ValueError):impedance([0,0],'source')
    def test_grounded_source_requires_zero_sequence(self):
        with self.assertRaises(ValueError):validate({'buses':[{'id':'a'}],'sources':[{'id':'s','bus':'a','grounded':True}]})
    def test_validation_copies(self):
        n={'buses':[{'id':'a'}]};validate(n);self.assertNotIn('base_kv',n['buses'][0])
