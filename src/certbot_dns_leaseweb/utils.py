""" A small collection of helpers for dns-01 challenges.
"""


def to_fqdn(name: str) -> str:
    """ Append trailing dot to FQDN-like DNS records lacking it.

    :param name: the DNS record name to attempt to convert to a FQDN.
    """

    if "." in name and not name.endswith("."):
        return f"{name}."

    return name
