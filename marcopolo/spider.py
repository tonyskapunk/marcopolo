import json
import base64

import requests

class Spider(object):
    """ Spider:
    Look for .polo files in a github endpoint and return a dictionary of url/yml files.
    """
    def __init__(self, api_endpoint, oauth_token):
        """
        Create Spider:

        Arguments
        =========
        api_endpoint: https url to github api base 
                (api.github.com or github.domain.com/api/)
        oauth_token: github oauth token with roles: ?
        
        """
        self.endpoint = api_endpoint
        self.session = requests.Session()
        self.session.headers['Authorization'] = 'token ' + oauth_token
        
        self.polos = []
        links = "{}/search/code?q=filename:polo%20extension:polo".format(self.endpoint)
        while links:
            print '-- loop top --'
            r = self.session.get(links)
            try:
                r.raise_for_status()
            except:
                raise
            if 'next' in r.links.keys():
                links = r.links['next']
            else:
                links = False
            d = r.json()['items']
            for x in d:
                self.polos.append(x['url'])

    def retrieve_polos(self):
        """
        retrieve_polos is a generator that returns urls and polo file strings

        yields tuples of (url, polo_data)
        """
        for x in self.polos:
            r = self.session.get(x)
            try:
                r.raise_for_status()
            except:
                raise
            polo = base64.b64decode(r.json()['content'])
            url = r.json()['url']
            yield (url, polo)
