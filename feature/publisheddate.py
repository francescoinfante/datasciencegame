from api import FeatureExtractorI
from datetime import timedelta
from dateutil.relativedelta import relativedelta


class PublishedDate(FeatureExtractorI):
    def __init__(self):
        self.attributes = {
            'monthly': 'numeric',
            'quarterly': 'numeric',
            'annually': 'numeric',
            #'biannually': 'numeric',
            'seconds': 'numeric'
        }

    def extract(self, data):
        pub_date = data["published_at"].replace(hour=0, minute=0, second=0, microsecond=0)
        first_of_month = pub_date - relativedelta(days=data["published_at"].day - 1)
        firs_of_year = first_of_month - relativedelta(months=first_of_month.month - 1)
        return {
            'monthly': first_of_month.strftime('%s'),
            'quarterly': (first_of_month - relativedelta(month=(first_of_month.month - 1) / 3 * 3 + 1)).strftime('%s'),
            'annually': firs_of_year.strftime('%s'),
            'biannually': (firs_of_year if firs_of_year.year % 2 else firs_of_year - relativedelta(years=1)).strftime('%s'),
            'seconds': pub_date.strftime('%s'),
        }
