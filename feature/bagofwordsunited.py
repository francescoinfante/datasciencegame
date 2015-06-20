from collections import Counter

from feature.api import FeatureExtractorI
from utility import tokenize


class BagOfWordsUnited(FeatureExtractorI):
    def __init__(self, train_sample, at_most=600):
        cnt = Counter()
        for _, given_features, _ in train_sample:
            cnt[given_features['title']] += 1
            cnt[given_features['description']] += 1

        self.attributes = dict([(x, 'numeric') for x in cnt.most_common(at_most)])

    def extract(self, data):
        tokens = tokenize(data['title'])
        tokens_desc = tokenize(data['description'])

        res = {}
        for x in tokens:
            res[x] = 1
        for x in tokens_desc:
            res[x] = 1

        return res
