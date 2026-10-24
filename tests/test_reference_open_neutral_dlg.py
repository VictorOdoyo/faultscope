import unittest
import numpy as np

import json,math
from pathlib import Path
from faultscope.solver import analyze
class ReferenceCase(unittest.TestCase):
    def test_phase_domain_oracle(self):
        c=json.loads((Path(__file__).parents[1]/'benchmarks/open_neutral_dlg.json').read_text());r=analyze(c['network'],bus='fault',fault_type=c['fault_type'],fault_z=c['fault_z'])
        for i,v in enumerate(r['fault']['phase_currents_a']):
            self.assertAlmostEqual(v['real'],c['expected']['fault_current_real_a'][i],delta=2e-5)
            self.assertAlmostEqual(v['imag'],c['expected']['fault_current_imag_a'][i],delta=2e-5)
        for i,b in enumerate(r['buses']):
            base=b['base_kv']*1000/math.sqrt(3)
            for j,v in enumerate(b['phase_voltage_v']):
                self.assertAlmostEqual(v['real']/base,c['expected']['bus_voltage_real_pu'][i][j],delta=2e-8)
                self.assertAlmostEqual(v['imag']/base,c['expected']['bus_voltage_imag_pu'][i][j],delta=2e-8)
