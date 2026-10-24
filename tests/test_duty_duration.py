import unittest
from faultscope.duty import duty


class DutyDurationTests(unittest.TestCase):
    def test_negative_unbalanced_duration_is_not_a_rating_pass(self):
        network = {'buses': [{'id': 'a'}],
                   'sources': [{'id': 's', 'bus': 'a', 'z0': [.01, .1]}]}
        with self.assertRaises(ValueError):
            duty(network, fault_type='slg', duration_s=-1)
