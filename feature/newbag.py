from feature.api import FeatureExtractorI
from utility import tokenize


class NewBag(FeatureExtractorI):
    def __init__(self, train_sample, ngram_size, list_of_attributes, progressbar):
        self.feat_set = set()
        self.ngram_size = ngram_size
        self.list_of_attributes = list_of_attributes
        for _, data, _ in train_sample:
            for attr in self.list_of_attributes:
                for token in tokenize(data[attr], self.ngram_size):
                    self.feat_set.add(token)
            progressbar.update(progressbar.currval + 1)

        self.attributes = dict([(x, 'numeric') for x in self.feat_set])

    def extract(self, data):
        tokens = []

        for attr in self.attributes:
            tokens.extend(tokenize(data[attr], self.ngram_size))

        return {key: 1 for key in tokens}
