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
