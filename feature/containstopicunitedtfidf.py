from collections import Counter
import math
import logging

from api import FeatureExtractorI


class ContainsTopicUnitedTFIDF(FeatureExtractorI):
    def __init__(self, train_sample, test_sample, normalization=False):
        self.cnt = Counter()
        for (_, given_features, _) in train_sample:
            for key in given_features['topicIds'] | given_features['relevantTopicIds']:
                self.cnt[key] += 1

        self.idf = Counter()

        for key in self.cnt:
            self.idf[key] = math.log(float(len(train_sample)) / self.cnt[key], 2)

        self.attributes = dict([(x, 'numeric') for x in self.idf])

        logging.info('ContainsTopicUnitedTFIDF init done')
        logging.info('Total number of attributes ' + str(len(self.idf)))
        logging.info(self.idf)

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

        topics = data['topicIds'] | data['relevantTopicIds']

        res = {key: '1' for key in topics}

        for x in res:
            res[x] /= float(len(topics))
            res[x] *= self.idf[x]
            if norm and self.normalization:
                res[x] /= self.max_value

        return res
