import datetime

from dingus import Dingus

from jsonrequester import *

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
