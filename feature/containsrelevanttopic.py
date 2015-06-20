from collections import Counter

from api import FeatureExtractorI


class ContainsRelevantTopic(FeatureExtractorI):
    def __init__(self, train_sample, at_most=200):
        cnt = Counter()
        for (_, given_features, _) in train_sample:
            for key in given_features['relevantTopicIds']:
                cnt[key] += 1
        self.attributes = {key: 'numeric' for (key, _) in cnt.most_common(at_most)}

    def extract(self, data):
        return {key: '1' for key in data['relevantTopicIds']}
