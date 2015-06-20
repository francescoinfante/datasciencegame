from collections import Counter

from api import FeatureExtractorI


class ContainsTopicUnited(FeatureExtractorI):
    def __init__(self, train_sample, min_freq=2):
        cnt = Counter()
        for (_, given_features, _) in train_sample:
            for key in given_features['topicIds']:
                cnt[key] += 1
            for key in given_features['relevantTopicIds']:
                cnt[key] += 1
        self.attributes = {key: 'numeric' for (key, value) in cnt if value >= min_freq}

    def extract(self, data):
        return {key: '1' for key in data['topicIds'] | data['relevantTopicIds']}
