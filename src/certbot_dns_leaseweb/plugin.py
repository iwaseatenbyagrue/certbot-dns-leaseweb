""" DNS Authenticator plugin for Leaseweb DNS. """

import requests
import zope.interface

from certbot import errors
from certbot import interfaces
from certbot.plugins import dns_common

from certbot_dns_leaseweb.client import (
    LeasewebClient,
    LeasewebException,
)


@zope.interface.implementer(interfaces.IAuthenticator)
@zope.interface.provider(interfaces.IPluginFactory)
class LeasewebAuthenticator(dns_common.DNSAuthenticator):
    """ DNS Authenticator for Leaseweb.

    This Authenticator uses the Leasweb Domains API to complete dns-01
    challenges.
    """

    description = "Obtain certificates using a DNS TXT record (if using Leaseweb DNS)."

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.credentials = None


    @classmethod
    def add_parser_arguments(cls, add): # pylint: disable=arguments-differ
        super().add_parser_arguments(add)
        add('credentials', help='Leaseweb credentials INI file.')


    def more_info(self) ->str:
        """ A human-readable string to inform users of what this plugin does.
        """
        return "This plugin completes dns-01 challenges using "\
               "the Leaseweb Domains API to configure DNS TXT records."


    def _setup_credentials(self):
        self.credentials = self._configure_credentials(
            "credentials",
            "Leaseweb credentials INI file",
            {
                "api_token":
                    "an API token obtained from 'https://secure.leaseweb.com/api-client-management/'", # pylint: disable=line-too-long
            },
        )


    def _perform(self, domain: str, validation_name: str, validation: str):
        try:
            self._get_client().add_record(
                domain,
                validation_name,
                [validation],
            )
        except (
                requests.ConnectionError,
                LeasewebException,
        ) as exception:
            raise errors.PluginError(exception)


    def _cleanup(self, domain: str, validation_name: str, validation: str):
        self._get_client().delete_record(
            domain,
            validation_name,
        )


    def _get_client(self):
        return LeasewebClient(self.credentials.conf("api_token"))
