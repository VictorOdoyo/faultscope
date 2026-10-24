import unittest
import numpy as np

from faultscope.studies import run
class StudyTests(unittest.TestCase):
    def test_invalid_action(self):
        with self.assertRaises(ValueError):run({},'invented')
    def test_provenance(self):
        s=run({'buses':[{'id':'a'}],'sources':[{'id':'s','bus':'a'}]});self.assertEqual(len(s['provenance']['model_sha256']),64)
