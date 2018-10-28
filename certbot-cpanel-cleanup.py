#!/usr/local/bin/python

import os, json, sys
from CpanelDnsUpdater import CpanelDnsUpdater

with open('secrets.json', 'r') as jsonFile:
    secrets = json.load(jsonFile)
    dns = CpanelDnsUpdater(
        secrets['cpanelHost'],
        secrets['cpanelDomain'],
        secrets['cpanelUsername'],
        secrets['cpanelPassword']
    )

certbot_domain = os.environ['CERTBOT_DOMAIN']
certbot_validation = os.environ['CERTBOT_VALIDATION']

record = {
    'name': certbot_domain + '.',
    'type': 'TXT'
}
result = dns.removeRecord(record)

if result:
    print('Successfully removed record ' + json.dumps(record))
else:
    print('Failed to remove record ' + json.dumps(record))
    sys.exit(-1)
