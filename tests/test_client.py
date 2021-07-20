"""
Unit tests for LeasewebClient
"""

import unittest

import requests_mock

from certbot_dns_leaseweb.client import (
    LeasewebClient,
    LEASEWEB_DOMAIN_API_ENDPOINT
)


class LeasewebClientTest(unittest.TestCase):
    """ Test suite for certbot_dns_leaseweb.client.LeasewebClient.
    """

    record_domain = "test.test"
    record_name = "test"
    record_content = ["test content"]
    record_ttl = 60

    api_token = "notarealtoken"

    def setUp(self):
        self.client = LeasewebClient(self.api_token)

    def test_add_record(self):
        """ feature: create a DNS record.

        Given a domain name, a record name, and some content
        When I add a new DNS record
        Then a new DNS record should be created
        And it should be of type 'TXT' by default.
        """
        with requests_mock.Mocker() as mock:
            mock.post(
                str(
                    f"{LEASEWEB_DOMAIN_API_ENDPOINT}"
                    f"/{self.record_domain}/resourceRecordSets"
                ),
                status_code=201,
            )
            # Default type and ttl
            self.client.add_record(
                self.record_domain,
                self.record_name,
                self.record_content
            )
            # Explicit type and TTL
            self.client.add_record(
                self.record_domain,
                self.record_name,
                self.record_content,
                "TXT",
                self.record_ttl
            )

    def test_delete_record(self):
        """ feature: delete a DNS record

        Given a domain name and a record name
        When I delete a DNS record
        Then the DNS record should be removed
        And it should be of type 'TXT' by default.
        """
        with requests_mock.Mocker() as mock:
            mock.delete(
                (
                    f"{LEASEWEB_DOMAIN_API_ENDPOINT}/"
                    f"{self.record_domain}/resourceRecordSets/"
                    f"{self.record_name}/TXT"
                ),
                status_code=204,
            )
            # Default type
            self.client.delete_record(
                self.record_domain,
                self.record_name,
            )
            # Explicit type
            self.client.delete_record(
                self.record_domain,
                self.record_name,
                "TXT",
            )


if __name__ == '__main__':
    unittest.main()
