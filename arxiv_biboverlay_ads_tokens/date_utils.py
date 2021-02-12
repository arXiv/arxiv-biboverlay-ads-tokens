from datetime import datetime, timedelta, timezone

utc_zone = timezone.utc


def get_date(timestr=None):
    """
    Always parses the time to be in the UTC time zone; or returns
    the current date (with UTC timezone specified)

    Originally from adsmicroservicesutils.adsmutils

    :param: timestr
    :type: str or None

    :return: datetime object with tzinfo=tzutc()
    """
    if timestr is None:
        return datetime.utcnow().replace(tzinfo=utc_zone)

    if isinstance(timestr, datetime):
        date = timestr
    else:
        date = parser.parse(timestr)

    if u'tzinfo' in repr(date):  # hack, around silly None.encode()...
        date = date.astimezone(utc_zone)
    else:
        # this depends on current locale, for the moment when not
        # timezone specified, I'll treat them as UTC (however, it
        # is probably not correct and should work with an offset
        # but to that we would have to know which timezone the
        # was created)

        # local_date = date.replace(tzinfo=local_zone)
        # date = date.astimezone(utc_zone)

        date = date.replace(tzinfo=utc_zone)

    return date


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
