# -*- coding: utf-8 -*-

import datetime
import time
from dateutil.tz import tzoffset


def str2date(strdate: str) -> datetime.datetime:
    # format: "%Y-%m-%dT%H:%M:%S.%fZ"
    # example: "2023-10-13T18:14:15.000Z"
    return datetime.datetime.fromisoformat(
        strdate[:-1] +
        "+00:00"  # FIXME
    )
    # return datetime.datetime.strptime(
    #     strdate,
    #     "%Y-%m-%dT%H:%M:%S.%fZ"
    # )


def date2str(date: datetime.datetime) -> str:
    return date.strftime("%Y-%m-%dT%H:%M:%S.%fZ")


timezone_config = ""


def current_time():
    # TODO: config modes to set timezone
    offset = time.timezone \
        if (time.localtime().tm_isdst == 0) \
        else time.altzone
    timezone = tzoffset("UTC+0", offset)
    return datetime.datetime.now(timezone)


if __name__ == "__main__":
    import time
    offset = time.timezone if (
        time.localtime().tm_isdst == 0) else time.altzone
    print(current_time())
    print(current_time().tzinfo)
    print(offset)
