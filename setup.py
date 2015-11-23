#!/usr/bin/python

import os
from setuptools import setup

NAME = "marcopolo"
SHORT_DESC = "Application and Load Balancer agnostic status tool"
VERSION = '0.1.0'
AUTHOR = 'Rackspace'
AUTHOR_EMAIL = 'cit-ops@rackspace.com'
LICENSE = 'ASLv2'


if __name__ == "__main__":

    with open('requirements.txt') as f:
        required_pkgs = f.read().splitlines()

    setup(
	name = NAME,
        version = VERSION,
        author = AUTHOR,
        author_email = AUTHOR_EMAIL,
        url = "https://github.com/rackerlabs/%s" % NAME,
        license = LICENSE,
        packages = [NAME],
        package_dir = {NAME: NAME},
        description = SHORT_DESC,
        entry_points={
            'console_scripts': [ 'marcopolo = marcopolo.util:run' ],
        },
	data_files=[('/etc/init.d', ['scripts/marcopolod.init']),
                    ('/usr/lib/systemd/system', ['scripts/marcopolod.service']),
                    ('/etc', ['marcopolo.conf']),],
        install_requires = required_pkgs
    )

