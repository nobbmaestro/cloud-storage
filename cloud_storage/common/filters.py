"""Collection of Jinja Filters."""

import datetime
import math

from babel.dates import format_timedelta


def pretty_file_size_format(file_size: str) -> str:
    """Pretty `file_size` format."""
    suffix = ("", "k", "M", "G", "T")
    size = int(file_size)

    # Format only non-zero values
    if size > 0:
        base = int(math.log(size, 1000))
        ret = "%3.1f %sB" % (size / (1000**base), suffix[base])

    else:
        ret = "-"

    return ret


def pretty_relative_datetime_format(time_stamp: datetime.datetime) -> str:
    """Pretty relatative `time_stamp` format."""
    delta = datetime.datetime.utcnow() - time_stamp
    return "%s ago" % format_timedelta(delta, locale="en_US")
