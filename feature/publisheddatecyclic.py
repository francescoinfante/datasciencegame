from dateutil.relativedelta import relativedelta

from api import FeatureExtractorI
from datetime import datetime
import time


class PublishedDateCyclic(FeatureExtractorI):
    def __init__(self):
        self.attributes = {
            'day': 'numeric',
            'week': 'numeric',
            'month': 'numeric',
            'year': 'numeric'
        }

    def extract(self, data):
        pub_date = data["published_at"].replace(second=0, microsecond=0)
        day = pub_date.replace(hour=0, minute=0)
        week = day - relativedelta(days=day.weekday())
        month = day.replace(day=1)
        year = month.replace(month=1)
        return {
            'day': int(time.mktime(pub_date.timetuple()) - time.mktime(day.timetuple())) / 60,  # minuti
            'week': int(time.mktime(pub_date.timetuple()) - time.mktime(week.timetuple())) / 3600,  # ore
            'month': int(time.mktime(pub_date.timetuple()) - time.mktime(month.timetuple())) / 3600,  # ore
            'year': int(time.mktime(pub_date.timetuple()) - time.mktime(year.timetuple())) / 86400,  # giorni
        }
