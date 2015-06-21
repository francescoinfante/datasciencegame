from api import FeatureExtractorI


class ExactDuration(FeatureExtractorI):
    def __init__(self, train_sample, test_sample):
        maximum = 1
        for instance in train_sample[1] + test_sample[1]:
            maximum = max(maximum, instance['exactduration'])
        self.maximum = maximum
        self.attributes = {'exactduration': 'numeric'}

    def extract(self, data):
        return {'exactduration': float(data['duration']) / self.maximum if data['duration'] != 0 else 0}
