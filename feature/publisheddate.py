import logging

from dateutil.relativedelta import relativedelta

from utility import date2int

from api import FeatureExtractorI


class PublishedDate(FeatureExtractorI):
    def __init__(self, train_sample, test_sample, normalize=False):
        maximums = {'monthly': 1, 'quarterly': 1, 'annually': 1, 'biannually': 1, 'days': 1}

        if normalize and train_sample and test_sample:
            for instance in train_sample + test_sample:
                instance = instance[1]
                pub_date = instance["published_at"].replace(hour=0, minute=0, second=0, microsecond=0)
                first_of_month = pub_date - relativedelta(days=instance["published_at"].day - 1)
                firs_of_year = first_of_month - relativedelta(months=first_of_month.month - 1)

                maximums['monthly'] = max(maximums['monthly'], date2int(first_of_month, 'd'))
                maximums['quarterly'] = max(maximums['quarterly'], date2int(
                    first_of_month - relativedelta(month=(first_of_month.month - 1) / 3 * 3 + 1), 'd'))
                maximums['annually'] = max(maximums['annually'], date2int(firs_of_year, 'd'))
                maximums['biannually'] = max(maximums['biannually'], date2int(
                    firs_of_year if firs_of_year.year % 2 else firs_of_year - relativedelta(years=1), 'd'))
                maximums['days'] = max(maximums['days'], date2int(instance["published_at"], 'd'))
            logging.info(__name__ + ' with normalization')
        else:
            logging.info(__name__ + ' with NO normalization')

        self.maximums = maximums

        self.attributes = {
            'monthly': 'numeric',
            'quarterly': 'numeric',
            'annually': 'numeric',
            # 'biannually': 'numeric',
            'days': 'numeric'
        }

    def extract(self, data):
        pub_date = data["published_at"].replace(hour=0, minute=0, second=0, microsecond=0)
        first_of_month = pub_date - relativedelta(days=data["published_at"].day - 1)
        firs_of_year = first_of_month - relativedelta(months=first_of_month.month - 1)
        return {
            'monthly': float(date2int(first_of_month, 'd')) / self.maximums['monthly'],
            'quarterly': float(
                date2int(first_of_month - relativedelta(month=(first_of_month.month - 1) / 3 * 3 + 1), 'd')) /
                         self.maximums['quarterly'],
            'annually': float(date2int(firs_of_year, 'd')) / self.maximums['annually'],
            'biannually': float(
                date2int(firs_of_year if firs_of_year.year % 2 else firs_of_year - relativedelta(years=1), 'd')) /
                          self.maximums['biannually'],
            'days': float(date2int(data["published_at"], 'd')) / self.maximums['days'],
        }
