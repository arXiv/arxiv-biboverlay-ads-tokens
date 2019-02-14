from adsmutils import get_date
from datetime import datetime
from dateutil import tz

from sqlalchemy import types

utc_zone = tz.tzutc()

class UTCDateTime(types.TypeDecorator):

    impl = types.DateTime
    def process_bind_param(self, value, engine):
        if value is not None:
            if isinstance(value, basestring):
                value = get_date(value)
            return value.astimezone(utc_zone)
    def process_result_value(self, value, engine):
        if value is not None:
            if isinstance(value, basestring):
                value = get_date(value)
            return value.replace(tzinfo=utc_zone)

def now():
    return datetime.utcnow().replace(tzinfo=utc_zone)
