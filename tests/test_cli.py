import unittest
import numpy as np

import sys,subprocess,json
class CLITests(unittest.TestCase):
    def test_packaged_examples(self):
        p=subprocess.run([sys.executable,'-m','faultscope','examples'],capture_output=True,text=True,check=True);self.assertGreater(len(json.loads(p.stdout)),2)
    def test_missing_case(self):
        p=subprocess.run([sys.executable,'-m','faultscope','study','example:unknown'],capture_output=True,text=True);self.assertEqual(p.returncode,2)
