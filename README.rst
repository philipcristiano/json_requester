JSONRequester
=============

JSONRequester is a wrapper around Httplib2 to interact with JSON APIs. It works
similarly to Httplib2 but converts request and response data to and from JSON.

Installing
----------

    pip install jsonrequester

Create a new requester
----------------------

    from jsonrequester import JsonRequester

    requester = JsonRequester('http://example.com')

Make a request
--------------

    requester.post('/post_handler', {'example': 'data'})

Methods
-------

Methods for ``GET`` and ``POST`` are provided as ``.get`` and ``.post`` methods on the
requester. Any additional HTTP methods you need can be made using the ``request`` method
on the requester.

    requester.request('PUT', '/put_handler', {'example': 'data'})
