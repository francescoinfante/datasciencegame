import time
from datetime import datetime

from dateutil.relativedelta import relativedelta

granularity = {
    's': 1,
    'm': 60,
    'h': 60*60,
    'd': 24*60*60,
}

def date_diff(date1, date2, part='s'):
    if part not in granularity:
        part = 's'

    return int(time.mktime(date1.timetuple()) - time.mktime(date2.timetuple())) / granularity[part]

def date2int(date, part='m'):
    return date_diff(date, datetime(2005, 1, 1, 0, 0), part)
