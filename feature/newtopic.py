from collections import Counter

from api import FeatureExtractorI


class NewTopic(FeatureExtractorI):
    def __init__(self, train_sample, progressbar):
        self.cnt = Counter()
        for _, given_features, _ in train_sample:
            for key in given_features['topicIds'] | given_features['relevantTopicIds']:
                self.cnt[key] += 1
            progressbar.update(progressbar.currval + 1)

        self.attributes = dict([(x, 'numeric') for x in self.cnt])

    def extract(self, data):
        topics = data['topicIds'] | data['relevantTopicIds']

        return {key: 1 for key in topics}
