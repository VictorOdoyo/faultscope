import unittest
import numpy as np

from faultscope.model import validate
from faultscope.sequence_networks import build
class SequenceNetworkTests(unittest.TestCase):
    def sample(self):return validate({'buses':[{'id':'a'},{'id':'b'}],'branches':[{'id':'t','from':'a','to':'b','kind':'transformer','from_winding':'D','to_winding':'Yg','z0':[0,.2]}]})
    def test_delta_blocks_zero_transfer(self):
        y=build(self.sample(),0);self.assertAlmostEqual(abs(y[0,1]),0);self.assertAlmostEqual(y[1,1].imag,-5)
    def test_negative_shift_is_opposite(self):
        n=self.sample();n['branches'][0]['shift_deg']=30
        self.assertAlmostEqual(np.angle(build(n,1)[0,1]/build(n,2)[0,1]),np.deg2rad(60),places=6)
