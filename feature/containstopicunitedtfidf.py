from collections import Counter
import math

from api import FeatureExtractorI


class ContainsTopicUnitedTFIDF(FeatureExtractorI):
    def __init__(self, train_sample, at_most=1000):
        cnt = Counter()
        for (_, given_features, _) in train_sample:
            for key in given_features['topicIds'] | given_features['relevantTopicIds']:
                cnt[key] += 1

        self.idf = Counter()

        for key in self.cnt:
            self.idf[key] = math.log(float(len(train_sample)) / self.cnt[key], 2)

        self.attributes = {key: 'numeric' for (key, _) in cnt.most_common(at_most)}

    def extract(self, data):

        topics = data['topicIds'] | data['relevantTopicIds']

        res = {key: '1' for key in topics}

        for x in res:
            res[x] /= float(len(topics))
            res[x] *= self.idf[x]

        return res
