from collections import Counter

from feature.api import FeatureExtractorI
from utility import tokenize


class BagOfWordsUnited(FeatureExtractorI):
    def __init__(self, train_sample, at_most=1000):
        cnt = Counter()
        for _, data, _ in train_sample:
            tokens = tokenize(data['title'] + ' ' + data['description'])
            for x in tokens:
                cnt[x] += 1

        self.attributes = dict([(x, 'numeric') for x in cnt.most_common(at_most)])

    def extract(self, data):
        tokens = tokenize(data['title'] + ' ' + data['description'])

        res = {}
        for x in tokens:
            res[x] = 1

        return res
