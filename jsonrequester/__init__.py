import json

import httplib2


class JsonRequester(object):
    """A wrapper to make requests to an HTTP based JSON API.

    >>> requester = JsonRequester('http://api.example.com/v1')
    >>> requester.get('/my/api/url')
    {'content': 'my api results'}
    """

    def __init__(self, base_url):
        self.base_url = base_url
        self.http = httplib2.Http()

    def _get_full_url(self, url):
        """Join `url` with the `base_url`"""
        return '{0}{1}'.format(self.base_url, url)

    def get(self, url):
        return self.request('GET', url)

    def post(self, url, data=None):
        return self.request('POST', url, data)

    def request(self, method, url, data=None):
        headers = {}
        if data is not None:
            data = json.dumps(data)
            headers = {'Content-Type': 'application/json'}

        response, content = self.http.request(
            self._get_full_url(url),
            method,
            body=data,
            headers=headers,
        )

        if response['content-type'] == 'application/json' and content:
            return json.loads(content)
