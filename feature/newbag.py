from collections import Counter

from feature.api import FeatureExtractorI
from utility import tokenize


class NewBag(FeatureExtractorI):
    def __init__(self, train_sample, ngram_size, progressbar):
        self.cnt = Counter()
        self.ngram_size = ngram_size
        for _, data, _ in train_sample:
            tmp_set = set()
            for token in tokenize(data['title'] + ' ' + data['description'], self.ngram_size):
                tmp_set.add(token)
            for token in tmp_set:
                self.cnt[token] += 1
            progressbar.update(progressbar.currval + 1)

        self.attributes = dict([(x, 'numeric') for x in self.cnt])

    def extract(self, data, norm=True):
        tokens = tokenize(data['title'] + ' ' + data['description'], self.ngram_size)
        count = Counter()

        for x in tokens:
            count[x] += 1

        return dict(count)
