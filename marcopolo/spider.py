import json
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
        
        polos = []
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
                polos.append(x['url'])
        print repr(polos)

