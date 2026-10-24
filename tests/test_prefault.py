import unittest
import numpy as np

from faultscope.prefault import from_gridflow
class PrefaultTests(unittest.TestCase):
    def test_gridflow_adapter(self):self.assertEqual(from_gridflow({'converged':True,'buses':[{'id':'a','vm_pu':.98,'va_deg':-2}]}),{'a':[.98,-2]})
    def test_reject_failed_profile(self):
        with self.assertRaises(ValueError):from_gridflow({'converged':False})
