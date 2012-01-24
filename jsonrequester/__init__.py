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

    It can be passed a serialization function to handle objects which do
    not have a native JSON representation.  This defaults to
    :func:`default_serializer`.

    It can also be passed a timeout value that is passed to
    :class:`httplib2.Http` when creating the connection. Note that there is
    a known issue with :class:`httplib2.Http` that may cause the actual timeout
    to be double what is specified
    (http://code.google.com/p/httplib2/issues/detail?id=124).

    """
    def __init__(self, base_url, serializer=default_serializer, timeout=5):
        self.base_url = base_url
        self.http = httplib2.Http(timeout=timeout)
        self.serializer = serializer

    def _get_full_url(self, url):
        """Join `url` with the `base_url`"""
        return '{0}{1}'.format(self.base_url, url)

    def get(self, url, **kwargs):
        return self.request('GET', url, **kwargs)

    def post(self, url, data=None, **kwargs):
        return self.request('POST', url, data, **kwargs)

    def request(self, method, url, data=None, **kwargs):
        headers = {}
        if data is not None:
            data = json.dumps(data, default=self.serializer)
            headers = {'Content-Type': 'application/json'}
        headers.update(kwargs.pop('headers', {}))

        response, content = self.http.request(
            self._get_full_url(url),
            method,
            body=data,
            headers=headers,
            **kwargs
        )

        if (response['content-type'] == 'application/json' or
            response['content-type'] == 'application/javascript') and content:
            return json.loads(content)
