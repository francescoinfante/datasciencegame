import math
from collections import Counter
import logging

from feature.api import FeatureExtractorI
from utility import tokenize


class BagOfWordsUnitedTFIDF(FeatureExtractorI):
    def __init__(self, train_sample, test_sample, ngram_size, normalization=False, progressbar=None):
        self.idf = Counter()
        self.ngram_size = ngram_size
        for _, data, _ in train_sample:
            tmp_set = set()
            for token in tokenize(data['title'] + ' ' + data['description'], self.ngram_size):
                tmp_set.add(token)
            for token in tmp_set:
                self.idf[token] += 1
            progressbar.update(progressbar.currval + 1)

        for key in self.idf:
            self.idf[key] = math.log(float(len(train_sample)) / self.idf[key], 2)

        logging.info('BagOfWordsUnitedTFIDF init done')
        logging.info('Total number of attributes ' + str(len(self.idf)))
        logging.info(self.idf)

        self.attributes = dict([(x, 'numeric') for x in self.idf])
        self.normalization = normalization
        if normalization:
            self.max_value = 0.0

            logging.info('Computing max value')

            for _, data, _ in train_sample + test_sample:
                result = self.extract(data, norm=False)
                for _, val in result.iteritems():
                    self.max_value = max(self.max_value, val)

            logging.info('max value: ' + str(self.max_value))

    def extract(self, data, norm=True):
        tokens = tokenize(data['title'] + ' ' + data['description'], self.ngram_size)
        count = Counter()

        for x in tokens:
            count[x] += 1

        for x in count:
            count[x] /= float(len(tokens))
            count[x] *= self.idf[x]
            if norm and self.normalization:
                count[x] /= self.max_value

        return dict(count)
