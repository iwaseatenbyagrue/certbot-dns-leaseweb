FROM python:3.9-slim

RUN pip install --no-cache-dir certbot
COPY . ./
RUN pip install --no-cache-dir --use-feature=in-tree-build .

ENTRYPOINT ["/usr/local/bin/certbot", "--authenticator=dns-leaseweb", "--dns-leaseweb-credentials=/etc/letsencrypt/credentials/leaseweb.ini"]
CMD []
