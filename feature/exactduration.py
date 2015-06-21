from api import FeatureExtractorI


class ExactDuration(FeatureExtractorI):
    def __init__(self, train_sample, test_sample, normalize=False):
        self.normalize = normalize
        if normalize:
            maximum = 1
            for instance in zip(*train_sample)[1] + zip(*test_sample)[1]:
                maximum = max(maximum, instance['exactduration'])
            self.maximum = maximum
        self.attributes = {'exactduration': 'numeric'}

    def extract(self, data):
        if self.normalize:
            return {'exactduration': float(data['duration']) / self.maximum}
        else:
            return {'exactduration': data['duration']}
