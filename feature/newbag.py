from collections import Counter

from feature.api import FeatureExtractorI
from utility import tokenize


class NewBag(FeatureExtractorI):
    def __init__(self, train_sample, ngram_size, list_of_attributes, min_frequency, progressbar):
        self.count = Counter()
        self.ngram_size = ngram_size
        self.list_of_attributes = list_of_attributes
        for _, data, _ in train_sample:
            for attr in self.list_of_attributes:
                for token in tokenize(data[attr], self.ngram_size):
                    self.count[token] += 1
            progressbar.update(progressbar.currval + 1)
        self.attributes = {key: 'numeric' for key, value in self.count if value >= min_frequency}

    def extract(self, data):
        tokens = []

        for attr in self.list_of_attributes:
            tokens.extend(tokenize(data[attr], self.ngram_size))

        return {key: 1 for key in tokens}
