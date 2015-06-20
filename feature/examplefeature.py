from api import FeatureExtractorI


class ExampleFeature(FeatureExtractorI):
    def __init__(self):
        self.attributes = {'feat_name': 'numeric'}

    def extract(self, data):
        return {'feat_name': 0}
