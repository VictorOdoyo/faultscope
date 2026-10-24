import unittest
import numpy as np

from faultscope.scan import scan
class ScanTests(unittest.TestCase):
    def test_unsourced_bus_stays_failed(self):
        n={'buses':[{'id':'a'},{'id':'b'}],'sources':[{'id':'s','bus':'a','z0':[0,.1]}]}
        r=scan(n,['3ph']);self.assertTrue(r['results'][0]['solved']);self.assertFalse(r['results'][1]['solved'])
