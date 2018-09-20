#!/usr/bin/env python

import marcopolo.cli as cli

from marcopolo import cli, mapper

polos = []
for x in ['api','idm','pubsub']:
    polos.append(cli.parse_schema_file('/opt/app-root/src/examples/schema/{0}.polo'.format(x)))
