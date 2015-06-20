from dateutil.relativedelta import relativedelta

from api import FeatureExtractorI


class PublishedDate(FeatureExtractorI):
    def __init__(self):
        self.attributes = {
            'monthly': 'numeric',
            'quarterly': 'numeric',
            'annually': 'numeric',
            # 'biannually': 'numeric',
            'seconds': 'numeric'
        }

    def extract(self, data):
        pub_date = data["published_at"].replace(hour=0, minute=0, second=0, microsecond=0)
        first_of_month = pub_date - relativedelta(days=data["published_at"].day - 1)
        firs_of_year = first_of_month - relativedelta(months=first_of_month.month - 1)
        return {
            'monthly': int(first_of_month.strftime('%s')) / 86400,
            'quarterly': int(
                (first_of_month - relativedelta(month=(first_of_month.month - 1) / 3 * 3 + 1)).strftime('%s')) / 86400,
            'annually': int(firs_of_year.strftime('%s')) / 86400,
            'biannually': int(
                (firs_of_year if firs_of_year.year % 2 else firs_of_year - relativedelta(years=1)).strftime(
                    '%s')) / 86400,
            'seconds': int(data["published_at"].strftime('%s')) / 86400,
        }
