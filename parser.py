#!/usr/bin/env python

import os
from marcopolo import objects, spider


url = os.environ.get('GITHUB_URL')
oauth = os.environ.get('OAUTH_TOKEN')

results = spider.Spider(url, oauth).retrieve_polos()

polos = []
for x in results:
    print(x[0])
    polos.append(objects.parse(x[1]))
