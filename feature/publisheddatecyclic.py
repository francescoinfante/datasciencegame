import logging

from dateutil.relativedelta import relativedelta

from utility import date_diff
from api import FeatureExtractorI


class PublishedDateCyclic(FeatureExtractorI):
    def __init__(self, train_sample, test_sample, normalize=False):
        maximums = {'day': 1, 'week': 1, 'month': 1, 'year': 1}

        if normalize and train_sample and test_sample:
            for instance in train_sample + test_sample:
                instance = instance[1]
                pub_date = instance["published_at"].replace(second=0, microsecond=0)
                day = pub_date.replace(hour=0, minute=0)
                week = day - relativedelta(days=day.weekday())
                month = day.replace(day=1)
                year = month.replace(month=1)

                maximums['day'] = max(maximums['day'], date_diff(pub_date, day, 'm'))
                maximums['week'] = max(maximums['week'], date_diff(pub_date, week, 'h'))
                maximums['month'] = max(maximums['month'], date_diff(pub_date, month, 'h'))
                maximums['year'] = max(maximums['year'], date_diff(pub_date, year, 'd'))
            logging.info(__name__ + ' with normalization')
        else:
            logging.info(__name__ + ' with NO normalization')

        self.maximums = maximums

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
            'day': float(date_diff(pub_date, day, 'm')) / self.maximums['day'],
            'week': float(date_diff(pub_date, week, 'h')) / self.maximums['week'],
            'month': float(date_diff(pub_date, month, 'h')) / self.maximums['month'],
            'year': float(date_diff(pub_date, year, 'd')) / self.maximums['year'],
        }
