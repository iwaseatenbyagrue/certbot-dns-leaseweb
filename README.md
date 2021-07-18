certbot-dns-leaseweb
====================

A certbot plugin that automates the process of completing a dns-01 challenge
using Leaseweb's [Domain API](https://developer.leaseweb.com/api-docs/domains_v2.html).

Install
-------

`certbot-dns-leaseweb` should be installed via pip, in the same python
environment in which `certbot` is installed:

```
pip install certbot-dns-leaseweb
```

Usage
------

Use the following flags to `certbot` to use and control this plugin:

| Option | Description |
|--------|-------------|
| `--authenticator dns-leaseweb` | **required**, enable and use this plugin. |
| `--dns-leaseweb-credentials` | **required**, Leaseweb API credentials INI file. |
| `--dns-leaseweb-propagation-seconds` | optional, seconds to wait for DNS records to propagate. |


Credentials
------------

A suitable API token can be generated from https://secure.leaseweb.com/api-client-management/.

The token should then be stored in an INI file:

```
dns_leaseweb_api_token = notarealtoken
```

**CAUTION**: These API credentials should be carefully protected from exposure
and unauthorised access.

They could be used to complete DNS challenges, allowing potentially unauthorised
parties to obtain or revoke certificates for your domains.

Examples
--------

Obtain a wildcard certificate for `example.com`:

```
certbot certonly \
  --authenticator dns-leaseweb \
  --dns-leaseweb-credentials leaseweb.ini \
  -d '*.example.com'
```

Obtain a wildcard certificate for `example.com`, with extra time for propagation:

```
certbot certonly \
  --authenticator dns-leaseweb \
  --dns-leaseweb-credentials leaseweb.ini \
  --dns-leaseweb-propagation-seconds 600 \
  -d '*.example.com'
```

Docker
------

If you prefer to run certbot with the `dns-leaseweb` plugin in docker, you can
build a suitable image with `make image`.

The image comes with a partially-completed CLI as its entrypoint:

```
/usr/local/bin/certbot \
  --authenticator=dns-leaseweb \
  --dns-leaseweb-credentials=/etc/letsencrypt/credentials/leaseweb.ini
```


You will need to create a suitable credentials file for the plugin at
`/etc/letsencrypt/credentials/leaseweb.ini` for the instructions below to work.


You can then use it as:

```
docker run --rm -ti \
  --volume "/etc/letsencrypt:/etc/letsencrypt" \
  --volume "/var/lib/letsencrypt:/var/lib/letsencrypt" \
  certbot-dns-leaseweb:latest \
    certonly \
      --dns-leaseweb-propagation-seconds 600 \
      -d '*.example.com'
```

Thanks
------

To [Letsencrypt](https://letsencrypt.org/), and the EFF for [certbot](https://certbot.eff.org/).

This plugin is adapted from https://github.com/ctrlaltcoop/certbot-dns-hetzner,
whose README was also the template for this file.

https://github.com/m42e/certbot-dns-ispconfig was also consulted during
development of this plugin.
