"""
Unit tests for LeasewebClient
"""

import unittest

from unittest import mock

from certbot.compat import os
from certbot.plugins import dns_test_common
from certbot.plugins.dns_test_common import DOMAIN
from certbot.tests import util as test_util

from certbot_dns_leaseweb.plugin import (
    LeasewebAuthenticator
)

class LeasewebAuthenticatorTest(
    test_util.TempDirTestCase,
    dns_test_common.BaseAuthenticatorTest,
):
    """ Test suite for `certbot_dns_leaseweb.plugin.LeasewebAuthenticator`.
    """

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
        """ feature: performing a DNS challenge should create a DNS record.

        Given a DNS-01 challenge
        When the LeasewebAuthenticator is used
        Then a new TXT record should be added to the appropriate domain.
        """
        self.auth.perform([self.achall])
        self.mock_client.add_record.assert_called_with(
            DOMAIN, "_acme-challenge." + DOMAIN, mock.ANY
        )


    def test_cleanup(self):
        """ feature: cleaning up a DNS challenge should delete a DNS record.

        Given a DNS-01 challenge has been performed
        When the LeasewebAuthenticator is cleaning up
        Then a TXT record should be deleted from the appropriate domain.
        """

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
