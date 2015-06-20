from feature.api import FeatureExtractorI
from utility import tokenize


class BagOfWordsOfDescription(FeatureExtractorI):
    def __init__(self, train_sample):
        self.token_set = set()
        for _, given_features, _ in train_sample:
            self.token_set |= set(tokenize(given_features['description']))

        self.attributes = dict([(x, 'numeric') for x in self.token_set])

    def extract(self, data):
        tokens = tokenize(data['description'])

        res = {}
        for x in tokens:
            res[x] = 1

        return res
