"""
Unit tests for LeasewebClient
"""

import unittest
import unittest.mock as mock

from certbot import errors
from certbot.compat import os
from certbot.plugins import dns_test_common
from certbot.plugins.dns_test_common import DOMAIN
from certbot.tests import util as test_util

from certbot_dns_leaseweb.client import (
    LEASEWEB_DOMAIN_API_ENDPOINT
)
from certbot_dns_leaseweb.plugin import (
    LeasewebAuthenticator
)

class LeasewebAuthenticatorTest(
    test_util.TempDirTestCase,
    dns_test_common.BaseAuthenticatorTest,
):

    def setUp(self):
        super().setUp()

        path = os.path.join(self.tempdir, "file.ini")
        dns_test_common.write(
            {
                "leaseweb_dns_api_token": "notarealtoken",
            },
            path,
        )

        self.config = mock.MagicMock(
            leaseweb_dns_credentials=path,
            leaseweb_dns_propagation_seconds=0,
        )  # don't wait during tests
        self.auth = LeasewebAuthenticator(self.config, "leaseweb_dns")
        self.mock_client = mock.MagicMock()
        # _get_client | pylint: disable=protected-access
        self.auth._get_client = mock.MagicMock(return_value=self.mock_client)


    @test_util.patch_get_utility()
    def test_perform(self, unused_mock_get_utility):
        self.auth.perform([self.achall])
        self.mock_client.add_record.assert_called_with(
            DOMAIN, "_acme-challenge." + DOMAIN, mock.ANY
        )


    def test_cleanup(self):
        # _attempt_cleanup | pylint: disable=protected-access
        self.auth._attempt_cleanup = True
        self.auth.cleanup([self.achall])

        expected = [
            mock.call.delete_record(
                DOMAIN, "_acme-challenge." + DOMAIN
            )
        ]
        self.assertEqual(expected, self.mock_client.mock_calls)

if __name__ == '__main__':
    unittest.main()
