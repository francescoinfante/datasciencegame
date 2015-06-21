from api import FeatureExtractorI


class HourOfDate(FeatureExtractorI):
    def __init__(self, train_sample, test_sample, normalize=False):
        self.attributes = {
            'pub_hour': 'numeric'
        }

    def extract(self, data):
        return {
            'pub_hour': data["published_at"].hour
        }
