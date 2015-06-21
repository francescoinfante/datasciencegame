from collections import Counter

from api import FeatureExtractorI


class NewTopic(FeatureExtractorI):
    def __init__(self, train_sample, list_of_attributes, min_frequency, progressbar):
        self.count = Counter()
        self.list_of_attributes = list_of_attributes
        for _, data, _ in train_sample:
            for attr in self.list_of_attributes:
                for topic in data[attr]:
                    self.count[topic] += 1
            progressbar.update(progressbar.currval + 1)
        self.attributes = {key: 'numeric' for key, value in self.count if value >= min_frequency}

    def extract(self, data):
        topics = []

        for attr in self.list_of_attributes:
            topics.extend(data[attr])

        return {key: 1 for key in topics}
