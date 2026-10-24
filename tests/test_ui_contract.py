import unittest
import numpy as np

from importlib.resources import files
class UIContractTests(unittest.TestCase):
    def test_accessible_local_assets(self):
        html=files('faultscope').joinpath('web','index.html').read_text()
        for key in ['network','run','fields','results','options','model-json','undo']:self.assertIn('id="'+key+'"',html)
        self.assertNotIn('<script src="https://',html)
