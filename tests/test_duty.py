import unittest
import numpy as np

from faultscope.duty import duty
class DutyTests(unittest.TestCase):
    def test_unsupported_unbalanced_peak_is_null(self):
        n={'buses':[{'id':'a'}],'sources':[{'id':'s','bus':'a','z0':[.01,.1]}],'equipment':[{'id':'cb','bus':'a','making_ka_peak':100}]}
        r=duty(n,fault_type='slg');self.assertIsNone(r['equipment_duty'][0]['comparisons'][0]['within_rating'])
