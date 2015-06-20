from api import FeatureExtractorI


class ExactDuration(FeatureExtractorI):
    def __init__(self):
        self.attributes = {'exactduration': 'numeric'}

    def extract(self, data):
        return {'exactduration': data['duration']}
