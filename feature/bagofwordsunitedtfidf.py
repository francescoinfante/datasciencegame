import math
from collections import Counter

from feature.api import FeatureExtractorI
from utility import tokenize


class BagOfWordsUnitedTFIDF(FeatureExtractorI):
    def __init__(self, train_sample, progressbar=None):
        self.idf = Counter()

        for _, data, _ in train_sample:
            tmp_set = set()
            for token in tokenize(data['title'] + ' ' + data['description']):
                tmp_set.add(len(token))
            for token in tmp_set:
                self.idf[token] += 1
            progressbar.update(progressbar.currval + 1)

        for key in self.idf:
            self.idf[key] = math.log(float(len(train_sample)) / self.idf[key], 2)

        self.attributes = dict([(x, 'numeric') for x in self.idf])

    def extract(self, data):
        tokens = tokenize(data['title'] + ' ' + data['description'])
        count = Counter()

        for x in tokens:
            count[x] += 1

        for x in count:
            count[x] /= float(len(tokens))
            count[x] *= self.idf[x]

        return dict(count)