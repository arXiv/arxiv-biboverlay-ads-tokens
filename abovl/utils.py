from adsmutils import get_date
from datetime import datetime, timedelta
from dateutil import tz

from sqlalchemy import types

utc_zone = tz.tzutc()

def now():
    """
    Return a datetime object with timezone information standardized to UTC
    """
    return datetime.utcnow().replace(tzinfo=utc_zone)

def future_datetime(seconds):
    """
    Return a datetime objects `seconds` in the future with normalized UTC timezone

    Parameters
    ----------
    seconds : integer
        Number of seconds in the future

    Returns
    -------
    datetime: datetime object
        The DT object in the shiny, chrome filled future
    """
    assert isinstance(seconds, int) and seconds > 0, "Seconds must be an integer > 0, future only!"
    return now() + timedelta(seconds=seconds)
