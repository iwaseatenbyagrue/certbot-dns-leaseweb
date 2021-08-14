"""
Unit tests for utils
"""

import unittest

from certbot_dns_leaseweb import utils


class UtilTest(unittest.TestCase):
    """ Test suite for certbot_dns_leaseweb.utils.
    """

    def test_to_fqdn(self):
        """ feature: return . terminated name when not using shortnames.

        """

        test_cases = [
            {"in": "test", "out": "test"},
            {"in": "test.test", "out": "test.test."},
            {"in": "test.test.", "out": "test.test."},
        ]

        for test_case in test_cases:
            self.assertEqual(utils.to_fqdn(test_case["in"]), test_case["out"])
