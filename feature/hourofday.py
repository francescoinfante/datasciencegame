from api import FeatureExtractorI


class HourOfDate(FeatureExtractorI):
    def __init__(self):
        self.attributes = dict([('pub_hour' + str(i),'numeric') for i in range(0, 25)])

    def extract(self, data):
        return {'pub_hour' + str(data["published_at"].hour): 1}
