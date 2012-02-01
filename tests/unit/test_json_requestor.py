import datetime

from deterministic_dingus import Dingus, DingusWhitelistTestCase

from jsonrequester import *
import jsonrequester as mod

DATE = datetime.datetime(2000, 01, 01, 01, 00, 00)

####
##
## default_serializer
##
####

def when_serializing_datetime_should_return_isoformat():
    assert default_serializer(DATE) == DATE.isoformat()

def when_serializing_unknown_type_should_stringify():
    obj = Dingus('obj')
    assert default_serializer(obj) == str(obj)


####
##
## JsonRequester.__init__
##
####

class BaseCreatingJsonRequester(DingusWhitelistTestCase):

    module = mod
    module_mocks = ['httplib2']
    additional_mocks = ['url']

    def setup(self):
        DingusWhitelistTestCase.setup(self)

    def should_set_base_url(self):
        assert self.json_requester.base_url == self.url

    def should_set_http(self):
        assert self.json_requester.http is self.module.httplib2.Http()

    def should_create_Http_with_timeout(self):
        assert self.module.httplib2.Http.calls('()', timeout=5)


class WhenCreatingJsonRequesterWithDefaults(BaseCreatingJsonRequester):

    def setup(self):
        BaseCreatingJsonRequester.setup(self)

        self.json_requester = JsonRequester(self.url)

    def should_set_serializer_to_default_serializer(self):
        assert self.json_requester.serializer is default_serializer


class WhenCreatingJsonRequesterWithSerializer(BaseCreatingJsonRequester):

    additional_mocks = ['serializer']

    def setup(self):
        BaseCreatingJsonRequester.setup(self)

        self.json_requester = JsonRequester(
            self.url, serializer=self.serializer)

    def should_set_serializer(self):
        assert self.json_requester.serializer == self.serializer


class WhenCreatingJsonRequesterWithTimeout(BaseCreatingJsonRequester):

    additional_mocks = ['timeout']

    def setup(self):
        BaseCreatingJsonRequester.setup(self)

        self.json_requester = JsonRequester(self.url, timeout=self.timeout)

    def should_create_Http_with_timeout(self):
        assert self.module.httplib2.Http.calls('()', timeout=self.timeout)


####
##
## JsonRequester.request
##
####

class BaseRequestTestCase(DingusWhitelistTestCase):

    module = mod
    module_mocks = ['json', 'httplib2']
    additional_mocks = [
        'base_url', 'content', 'kwargs', 'method', 'response', 'url']

    def setup(self):
        DingusWhitelistTestCase.setup(self)
        self.old_get_full_url = JsonRequester._get_full_url
        JsonRequester._get_full_url = Dingus('_get_full_url')
        self.json_requester = JsonRequester(self.base_url)

    def teardown(self):
        JsonRequester._get_full_url = self.old_get_full_url


class PropertyNoDataProvided(object):

    def should_call_http_request_without_data(self):
        assert self.module.httplib2.Http().request.calls(
            '()',
            JsonRequester._get_full_url(),
            self.method,
            body=None,
            headers={},
        )


class PropertyDataProvided(object):

    def should_call_http_request_with_data(self):
        assert self.module.httplib2.Http().request.calls(
            '()',
            JsonRequester._get_full_url(),
            self.method,
            body=self.module.json.dumps(),
            headers={'Content-Type': 'application/json'},
        )


class WhenRequestReturnsApplicationJsonAndContentIsNotNone(
        BaseRequestTestCase, PropertyNoDataProvided):

    def setup(self):
        BaseRequestTestCase.setup(self)
        self.response['content-type'] = 'application/json'
        self.module.httplib2.Http().request.return_value = (
            self.response, self.content)

        self.returned = self.json_requester.request(self.method, self.url)

    def should_return_json(self):
        assert self.returned == self.module.json.loads()


class WhenRequestReturnsApplicationJavascriptAndContentIsNotNone(
        BaseRequestTestCase, PropertyNoDataProvided):

    def setup(self):
        BaseRequestTestCase.setup(self)
        self.response['content-type'] = 'application/javascript'
        self.module.httplib2.Http().request.return_value = (
            self.response, self.content)

        self.returned = self.json_requester.request(self.method, self.url)

    def should_return_json(self):
        assert self.returned == self.module.json.loads()


class WhenRequestReturnsApplicationJsonAndContentIsNone(
        BaseRequestTestCase, PropertyNoDataProvided):

    def setup(self):
        BaseRequestTestCase.setup(self)
        self.response['content-type'] = 'application/json'
        self.module.httplib2.Http().request.return_value = (
            self.response, None)

        self.returned = self.json_requester.request(self.method, self.url)

    def should_return_None(self):
        assert self.returned == None


class WhenRequestReturnsApplicationJavascriptAndContentIsNone(
        BaseRequestTestCase, PropertyNoDataProvided):

    def setup(self):
        BaseRequestTestCase.setup(self)
        self.response['content-type'] = 'application/javascript'
        self.module.httplib2.Http().request.return_value = (
            self.response, None)

        self.returned = self.json_requester.request(self.method, self.url)

    def should_return_None(self):
        assert self.returned == None


class WhenRequestDoesNotReturnApplicationJson(
        BaseRequestTestCase, PropertyNoDataProvided):

    def setup(self):
        BaseRequestTestCase.setup(self)
        self.response['content-type'] = 'not application/json'
        self.module.httplib2.Http().request.return_value = (
            self.response, self.content)

        self.returned = self.json_requester.request(self.method, self.url)

    def should_return_None(self):
        assert self.returned == None


class WhenRequestWithDataReturnsApplicationJsonAndContentIsNotNone(
        BaseRequestTestCase, PropertyDataProvided):

    additional_mocks = ['data']

    def setup(self):
        BaseRequestTestCase.setup(self)
        self.response['content-type'] = 'application/json'
        self.module.httplib2.Http().request.return_value = (
            self.response, self.content)

        self.returned = self.json_requester.request(
            self.method, self.url, self.data)

    def should_return_json(self):
        assert self.returned == self.module.json.loads()


class WhenRequestWithDataReturnsApplicationJsonWithCharsetAndContentIsNotNone(
        BaseRequestTestCase, PropertyDataProvided):

    additional_mocks = ['data']

    def setup(self):
        BaseRequestTestCase.setup(self)
        self.response['content-type'] = 'application/json; charset=UTF-8'
        self.module.httplib2.Http().request.return_value = (
            self.response, self.content)

        self.returned = self.json_requester.request(
            self.method, self.url, self.data)

    def should_return_json(self):
        assert self.returned == self.module.json.loads()


class WhenRequestWithDataReturnsApplicationJavascriptWithCharsetAndContentIsNotNone(
        BaseRequestTestCase, PropertyDataProvided):

    additional_mocks = ['data']

    def setup(self):
        BaseRequestTestCase.setup(self)
        self.response['content-type'] = 'application/javascript; charset=UTF-8'
        self.module.httplib2.Http().request.return_value = (
            self.response, self.content)

        self.returned = self.json_requester.request(
            self.method, self.url, self.data)

    def should_return_json(self):
        assert self.returned == self.module.json.loads()
