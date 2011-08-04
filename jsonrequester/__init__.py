import datetime
import json

import httplib2


def default_serializer(obj):
    """Handle serializing non JSON-native objects.

    By default :func:`json.dumps` raises a :class:`TypeError` when a value
    cannot be translated JSON in a standardized way.  It is helpful to
    serialize :class:`datetime.datetime` instances as ISO formatted date
    strings.

    For other unknown types this serializer will attempt to cast them as a string.

    """
    if isinstance(obj, datetime.datetime):
        return obj.isoformat()
    return str(obj)


class JsonRequester(object):
    """A wrapper to make requests to an HTTP based JSON API.

    >>> requester = JsonRequester('http://api.example.com/v1')
    >>> requester.get('/my/api/url')
    {'content': 'my api results'}

    It can also be passed a serialization function to handle objects which do
    not have a native JSON representation.  This defaults to
    :func:`default_serializer`.
    """

    def __init__(self, base_url, serializer=default_serializer):
        self.base_url = base_url
        self.http = httplib2.Http()
        self.serializer = serializer

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
            data = json.dumps(data, default=self.serializer)
            headers = {'Content-Type': 'application/json'}

        response, content = self.http.request(
            self._get_full_url(url),
            method,
            body=data,
            headers=headers,
        )

        if response['content-type'] == 'application/json' and content:
            return json.loads(content)
